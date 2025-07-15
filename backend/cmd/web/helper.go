// file: cmd/web/helpers.go
package main

import (
	"fmt"
	"net/http"
	"runtime/debug"

	"github.com/gin-gonic/gin"
)

// serverError 记录详细错误日志和堆栈跟踪，并向用户发送通用的500响应
func (app *application) serverError(c *gin.Context, err error) {
	trace := fmt.Sprintf("%s\n%s", err.Error(), debug.Stack())
	app.errorLog.Output(2, trace) // Output(2, ...) 能确保报告正确的文件和行号

	c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
}

// clientError 发送特定状态码和信息的客户端错误响应
func (app *application) clientError(c *gin.Context, status int, message string) {
	c.JSON(status, gin.H{"error": message})
}

// notFound 发送404 Not Found响应
func (app *application) notFound(c *gin.Context) {
	app.clientError(c, http.StatusNotFound, "The requested resource could not be found")
}
