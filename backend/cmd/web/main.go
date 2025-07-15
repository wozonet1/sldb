// file: cmd/web/main.go
package main

import (
	"database/sql"
	"flag"
	"log"
	"net/http"
	"os"

	"geneprediction.wozonet.net/pkg/models/mysql" // 使用您的模块路径
	_ "github.com/go-sql-driver/mysql"            // 导入MySQL驱动
)

// application 结构体用于依赖注入，方便在处理器之间共享连接池等资源
type application struct {
	errorLog    *log.Logger
	infoLog     *log.Logger
	predictions *mysql.PredictionModel
}

func main() {
	// 1. 配置命令行参数
	addr := flag.String("addr", ":5555", "HTTP network address")
	// DSN (Data Source Name) 格式: 'user:password@tcp(host:port)/dbname?parseTime=true'
	dsn := flag.String("dsn", "zhucj:Emakingir5!@tcp(localhost:3306)/gene_prediction?parseTime=true", "MySQL data source name")
	flag.Parse()

	// 2. 配置日志记录器
	infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)
	errorLog := log.New(os.Stderr, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

	// 3. 连接数据库
	db, err := openDB(*dsn)
	if err != nil {
		errorLog.Fatal(err)
	}
	defer db.Close()

	// 4. 初始化应用（依赖注入）
	app := &application{
		errorLog:    errorLog,
		infoLog:     infoLog,
		predictions: &mysql.PredictionModel{DB: db},
	}

	// 5. 配置并启动服务
	infoLog.Printf("Starting server on %s", *addr)
	// 创建一个自定义的服务器，可以设置超时等参数，比直接ListenAndServe更健壮
	srv := &http.Server{
		Addr:     *addr,
		ErrorLog: errorLog,
		Handler:  app.routes(), // 使用我们定义的路由
	}

	err = srv.ListenAndServe()
	errorLog.Fatal(err)
}

// openDB 封装了数据库连接池的创建和验证逻辑
func openDB(dsn string) (*sql.DB, error) {
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}
	// Ping() 用于验证与数据库的连接是否仍然存在，并建立连接（如果需要）
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return db, nil
}
