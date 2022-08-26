from app import create_app

config = {
    "base": "app.config.Base",
    "dev": "app.config.Development",
    "prod": "app.config.Production"
}

app = create_app(config)

if __name__ == "__main__":
    app.run()