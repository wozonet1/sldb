// file: cmd/web/helpers.go
package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

// serverError 记录详细错误日志并发送通用的500响应
func (app *application) serverError(c *gin.Context, err error) {
	trace := fmt.Sprintf("%s\n", err.Error())
	app.errorLog.Println(trace)
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
