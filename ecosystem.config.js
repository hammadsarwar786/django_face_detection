module.exports = {
  apps: [
    {
      name: "django-api",
      script: "manage.py",
      args: "runserver",
      watch: true,
      autorestart: true,
      env: {
        DJANGO_SETTINGS_MODULE: "myproject.settings",
      },
    },
  ],
};
