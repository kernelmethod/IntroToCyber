package main

import (
	"crypto/rand"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"malgo/core"
	"math/big"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"go.uber.org/zap"
)

func CreateRequest(logger *zap.Logger) (*http.Request, error) {
	var body io.Reader
	var host string
	method := ""
	body = nil

	// Determine the host that we're querying at random
	eventBig, err := rand.Int(rand.Reader, big.NewInt(100))
	if err != nil {
		return nil, err
	}
	event := eventBig.Int64()
	logger.Debug("Sampled random event", zap.Int64("event", event))

	if event <= 1 {
		// Make a POST request to a strange subdomain
		host = fmt.Sprintf("https://whataweirdsubdomain.%s", core.BaseDomain)
		method = "POST"
		bodyData, err := core.AnomalousData()
		if err != nil {
			return nil, err
		}
		body = strings.NewReader(bodyData)
	} else if event <= 20 {
		host = fmt.Sprintf("https://%s:5000", core.BaseDomain)
	} else {
		host = fmt.Sprintf("https://%s", core.BaseDomain)
	}

	if method == "" {
		if event%2 == 0 {
			method = "GET"
		} else {
			method = "POST"
			body = strings.NewReader("testing, testing!")
		}
	}

	logger.Debug("HTTP request params", zap.String("method", method), zap.String("host", host))
	req, err := http.NewRequest(method, host, body)
	if err != nil {
		return nil, err
	}

	if method == "POST" {
		req.Header.Add("Content-Type", "text/plain")
	}

	return req, nil
}

func RunDriver(logger *zap.Logger) error {
	var req *http.Request
	var resp *http.Response
	var err error

	// Make HTTP request based on UID
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{
		Timeout:   15 * time.Second,
		Transport: tr,
	}

	if req, err = CreateRequest(logger); err != nil {
		return err
	}

	if resp, err = client.Do(req); err != nil {
		return err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	logger.Debug("Retrieved body contents", zap.ByteString("body", body))

	return nil
}

// Inner loop of the driver function.
func DriverLoop(logger *zap.Logger, maxSleepTime int64) error {
	var err error

	// Wait a random amount of time before running the driver again
	sleepTimeBig, err := rand.Int(rand.Reader, big.NewInt(maxSleepTime))
	if err != nil {
		return err
	}
	sleepTime := sleepTimeBig.Int64()
	logger.Info("Starting sleep", zap.Int64("sleepTime", sleepTime))

	// Sleep before running driver
	time.Sleep(time.Duration(sleepTime) * time.Millisecond)
	logger.Info("Awaking from sleep")

	return RunDriver(logger)
}

func main() {
	var err error

	lvl := zap.LevelFlag("L", core.DefaultLogLevel, "log level")
	flag.Parse()

	zl, err := core.CreateZap(lvl)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to create logger: %s", err)
		os.Exit(1)
	}

	logger := zl.Named(core.ProjectName)
	maxSleepTime := int64(120 * 1000)

	if envMaxSleep := os.Getenv("MALGO_MAX_SLEEP"); envMaxSleep != "" {
		maxSleepTime, err = strconv.ParseInt(envMaxSleep, 10, 64)
		if err != nil {
			logger.Fatal("Unable to parse the MALGO_MAX_SLEEP environment variable", zap.Error(err))
			os.Exit(1)
		}
	}

	if err := DriverLoop(zl, maxSleepTime); err != nil {
		logger.Error("Error running driver inner loop", zap.Error(err))

		// Wait a few seconds before starting the next loop
		time.Sleep(5 * time.Second)
	}
}
