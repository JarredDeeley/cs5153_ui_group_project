#!/bin/sh

if [[ $1 == "start" ]]; then
  if [ -d "public" ]; then
    rm ./public/*
    echo
    echo "[+] Webpack Assets Compile and Flask Start"
    echo "[+] webpack -p --progress --config webpack.config.js && flask run"
    echo
    webpack -p --progress --config webpack.config.js
    flask run
  else
    mkdir public
    echo "[+] webpack -p --progress --config webpack.config.js && flask run"
    webpack -p --progress --config webpack.config.js
    flask run
  fi
elif [[ $1 == "start-dev" ]]; then
  if [ -d "public" ]; then
    echo
    echo "[+] Start Webpack Development Server and Flask Start"
    echo "[+] honcho start"
    echo
    honcho start
  else
    mkdir public
    echo
    echo "[+] Webpack Assets Compile and Flask Start"
    echo "[+] honcho start"
    echo
    honcho start
  fi
elif [[ $1 == "build" ]]; then
  if [ -d "public" ]; then
    rm ./public/*
    echo
    echo "[+] Webpack Assets Compile"
    echo "[+] webpack -p --progress --config webpack.config.js"
    echo
    webpack -p --progress --config webpack.config.js
  else
    mkdir public
    echo
    echo "[+] Webpack Assets Compile"
    echo "[+] webpack -p --progress --config webpack.config.js"
    echo
    webpack -p --progress --config webpack.config.js
  fi
elif [[ $1 == "dev-build" ]]; then
  if [ -d "public" ]; then
    rm ./public/*
    echo
    echo "[+] Webpack Assets Compile Dev Build"
    echo "[+] webpack -p --progress -d --config webpack.config.js"
    echo
    webpack -p --progress -d --config webpack.config.js
  else
    mkdir public
    echo
    echo "[+] Webpack Assets Compile Dev Build"
    echo "[+] webpack -p --progress -d --config webpack.config.js"
    echo
    webpack -p --progress --config webpack.config.js
  fi
elif [[ $1 == "watch" ]]; then
  if [ -d "public" ]; then
    rm ./public/*
    echo
    echo "[+] Webpack Watch Assets"
    echo "[+] webpack --progress -d --config webpack.config.js --watch"
    echo
    webpack --progress -d --config webpack.config.js --watch
  else
    mkdir public
    echo
    echo "[+] Webpack Watch Assets"
    echo "[+] webpack --progress -d --config webpack.config.js --watch"
    echo
    webpack --progress -d --config webpack.config.js --watch
  fi
fi
