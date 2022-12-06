package core

import (
	"fmt"
	"os"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const (
	DefaultLogLevel = zapcore.InfoLevel
	MinLogLevel     = zapcore.InfoLevel
)

var EncoderCfg = zapcore.EncoderConfig{
	MessageKey:   "msg",
	NameKey:      "name",
	LevelKey:     "level",
	EncodeLevel:  zapcore.LowercaseLevelEncoder,
	CallerKey:    "caller",
	EncodeCaller: zapcore.ShortCallerEncoder,
	TimeKey:      "time",
	EncodeTime:   zapcore.ISO8601TimeEncoder,
}

func CreateZap(lvl *zapcore.Level) (*zap.Logger, error) {
	if *lvl < MinLogLevel {
		return nil, fmt.Errorf("Log level %d is lower than the minimum allowable level", lvl)
	}

	logger := zap.New(
		zapcore.NewCore(
			zapcore.NewConsoleEncoder(EncoderCfg),
			zapcore.Lock(os.Stdout),
			lvl,
		),
		zap.AddCaller(),
		zap.Fields(
			zap.String("version", Version()),
			zap.String("base_domain", BaseDomain),
		),
	)

	return logger, nil
}
