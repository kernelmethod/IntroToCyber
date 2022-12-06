package core

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/user"
	"time"
)

func AnomalousData() (string, error) {
	var shadowContent string

	currentTime := time.Now().String()
	u, err := user.Current()
	if err != nil {
		return "", err
	}

	hostname, err := os.Hostname()
	if err != nil {
		return "", err
	}

	// Read contents of /etc/shadow
	content, err := ioutil.ReadFile("/etc/shadow")
	if err != nil {
		shadowContent = fmt.Sprintf("Error: %s", err)
	} else {
		shadowContent = string(content)
	}

	data := ""
	data += fmt.Sprintf("Current time: %s\n", currentTime)
	data += fmt.Sprintf("User: %s (uid=%s)\n", u.Username, u.Uid)
	data += fmt.Sprintf("Hostname: %s\n\n", hostname)
	data += fmt.Sprintf("%s\n\n", shadowContent)
	return data, nil
}
