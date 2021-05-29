import { Log } from "..";
import db from "./firebaseInit";

export async function getAllDataJSON(res: any) {
  const logs = await getAllData();
  let logsString = JSON.stringify(logs);

  res.setHeader("Content-disposition", "attachment; filename=logs.json");
  res.setHeader("Content-type", "application/json");
  res.write(logsString, function (err: any) {
    res.end();
  });
}

async function getAllData() {
  const logRef = db.collection("Logs");
  try {
    const logSnapshot = await logRef.get();

    let logs: Log[] = [];
    logSnapshot.forEach((doc) => {
      const data = doc.data();
      const docId = doc.id;
      const logItem: Log = {
        id: docId,
        answers: data.answers,
        createdAt: data.createdAt,
        screenSize: data.screenSize,
        touches: data.touches,
        tries: data.tries,
      };

      logs.push(logItem);
    });

    return logs;
  } catch (error) {
    console.log("@@@@ getAllData err", error);
    return [];
  }
}
