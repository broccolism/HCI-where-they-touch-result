import * as express from "express";
import { getAllDataJSON } from "./firebase/dataGetter";

function runServer() {
  const express = require("express");
  const app = express();
  const PORT = 8000;

  app.get("/", (req: any, res: any) => res.send("Express + TypeScript Server"));

  app.get("/data", (req: any, res: any) => getAllDataJSON(res));

  app.listen(PORT, () => {
    console.log(`⚡️[server]: Server is running at https://localhost:${PORT}`);
  });
}

runServer();

export interface Log {
  id: string;
  answers: LogAnswer;
  createdAt: Date;
  screenSize: LogScreenSize;
  touches: LogTouch[];
  tries: LogTry[];
}

interface LogAnswer {
  age: string;
  gender: string;
  typpingType: string;
}

interface LogScreenSize {
  height: number;
  width: number;
}

interface LogTouch {
  content: string;
  createdAt: string;
  pageX: string;
  pageY: string;
  path: string;
}

interface LogTry {
  tries: number;
  target: string;
}
