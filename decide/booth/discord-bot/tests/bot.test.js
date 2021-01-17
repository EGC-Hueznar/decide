const { group, test, command, beforeStart, afterAll } = require("corde");
const { client, loginBot } = require("../index.js");
const Discord = require('discord.js')

beforeStart(() => {
    loginBot();
  });

  group("must ping", () => {
    test("help", () => {
      command("ping").mustReturn("pong");
    });
  });
  
  afterAll(() => {
    client.destroy();
  });