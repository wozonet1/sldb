// file: cmd/web/main.go
package main

import (
	"database/sql"
	"flag"
	"log"
	"net/http"
	"os"

	"geneprediction.wozonet.net/pkg/models/mysql"
	_ "github.com/go-sql-driver/mysql" // 导入MySQL驱动
)

// application 结构体用于依赖注入
type application struct {
	errorLog    *log.Logger
	infoLog     *log.Logger
	predictions *mysql.PredictionModel
}

func main() {
	// 1. 配置
	addr := flag.String("addr", ":5555", "HTTP network address")
	// 格式: 'user:password@tcp(host:port)/dbname?parseTime=true'
	dsn := flag.String("dsn", "root:Emakingir5@tcp(localhost:3306)/your_database?parseTime=true", "MySQL data source name")
	flag.Parse()

	// 2. 日志
	infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)
	errorLog := log.New(os.Stderr, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

	// 3. 数据库连接
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

	// 5. 启动服务
	infoLog.Printf("Starting server on %s", *addr)
	err = http.ListenAndServe(*addr, app.routes()) // 使用我们定义的路由
	errorLog.Fatal(err)
}

// openDB 封装了数据库连接的逻辑
func openDB(dsn string) (*sql.DB, error) {
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return db, nil
}
