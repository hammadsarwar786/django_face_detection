module.exports = {
  apps: [
    {
      name: "django-api",
      script: "manage.py",
      args: "runserver 0.0.0.0:8000",
      watch: true,
      autorestart: true,
      interpreter: "/home/ubuntu/myenv/bin/python3",
      env: {
        DJANGO_SETTINGS_MODULE: "myproject.settings",
      },
    },
  ],
};
