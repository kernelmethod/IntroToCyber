package core

import (
	"fmt"
	"runtime"
)

var (
	BaseDomain     = "localhost"
	BuildTime      = "(N/A)"
	ProjectName    = "(N/A)"
	ProjectVersion = "dev"
)

func Version() string {
	return fmt.Sprintf("%s (%s %s)", ProjectVersion, runtime.Version(), BuildTime)
}
