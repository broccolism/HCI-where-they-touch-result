import * as express from "express";

function runServer() {
  const express = require("express");
  const app = express();
  const PORT = 8000;

  app.get("/", (req: any, res: any) => res.send("Express + TypeScript Server"));

  app.listen(PORT, () => {
    console.log(`⚡️[server]: Server is running at https://localhost:${PORT}`);
  });
}

runServer();
