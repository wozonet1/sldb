// file: cmd/web/routes.go
package main

import (
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func (app *application) routes() http.Handler {
	// 使用 ReleaseMode 可以获得更好的性能，并减少不必要的日志输出
	// gin.SetMode(gin.ReleaseMode)
	router := gin.Default()

	// 配置CORS中间件，允许所有来源，与之前的Flask版一致
	// 这对于前后端分离应用是必需的
	config := cors.DefaultConfig()
	config.AllowAllOrigins = true
	router.Use(cors.New(config))

	// 定义API路由组
	api := router.Group("/api/v1")
	{
		api.GET("/predict", app.predictHandler)
	}

	// 添加一个简单的健康检查路由
	router.GET("/healthcheck", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "available", "environment": "development"})
	})

	return router
}
