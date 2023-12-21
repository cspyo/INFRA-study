import { S3 } from "@aws-sdk/client-s3";
import https from "https";

const s3 = new S3();

const ENV = process.env;
if (!ENV.SLACK_WEB_HOOK)
  throw new Error("Missing environment variable: webhook");
const slackWebHook = ENV.SLACK_WEB_HOOK;

export const handler = async (event) => {
  console.log("EVENT: \n" + JSON.stringify(event, null, 2));
  const s3Object = await getS3Object(event);
  const message = new Message(event, s3Object);
  console.log("MESSAGE: \n" + JSON.stringify(message, null, 2));

  try {
    await sendToSlack(slackMessage(message), slackWebHook);
  } catch (e) {
    console.log("slack message failed: ", e);
    context.fail(e);
  }
};

export class Message {
  constructor(event, s3Object) {
    const { eventName, eventTime, userIdentity, requestParameters, s3 } =
      event.Records[0];
    this.eventName = eventName;
    this.eventTime = new KstTime(eventTime).time;
    this.userName = userIdentity.principalId.split(":")[2];
    this.userIp = requestParameters.sourceIPAddress;
    this.bucket = s3.bucket.name;
    this.fileKey = s3.object.key;
    this.objectContentType = s3Object.ContentType;
  }
}

export async function getS3Object(event) {
  const s3Params = processEventToS3Params(event);
  try {
    const s3Object = await s3.getObject(s3Params);
    return s3Object;
  } catch (e) {
    console.log(e);
    const message = `Error getting object ${s3Params.Key} from bucket ${s3Params.Bucket}.`;
    console.log(message);
    throw new Error(message);
  }
}

export function processEventToS3Params(event) {
  const bucket = event.Records[0].s3.bucket.name;
  const key = decodeURIComponent(
    event.Records[0].s3.object.key.replace(/\+/g, " ")
  );
  const s3Params = {
    Bucket: bucket,
    Key: key,
  };
  return s3Params;
}

export class KstTime {
  /**
   * @param dateString {string}
   */
  constructor(dateString) {
    const timestamp = new Date(dateString).getTime();
    const kst = new Date(timestamp + 32400000);
    this.time = `${kst.getFullYear().toString()}-${this.pad(
      kst.getMonth() + 1
    )}-${this.pad(kst.getDate())} ${this.pad(kst.getHours())}:${this.pad(
      kst.getMinutes()
    )}:${this.pad(kst.getSeconds())}`;
  }

  pad(n) {
    return n < 10 ? "0" + n : n;
  }
}

/** @param message {Message} */
export function slackMessage(message) {
  const title = `[${message.eventName} 발생]`;
  const payload = `언제: ${message.eventTime}\n사용자: ${message.userName}\n사용자IP: ${message.userIp}\n버킷이름: ${message.bucket}\n파일이름: ${message.fileKey}\n파일타입: ${message.objectContentType}`;

  const color = "#2eb886";

  return {
    attachments: [
      {
        color: color,
        title: title,
        fields: [
          {
            value: payload,
            short: false,
          },
        ],
      },
    ],
  };
}

export async function sendToSlack(message, webhook) {
  const { host, pathname } = new URL(webhook);
  const options = {
    hostname: host,
    path: pathname,
    method: "POST",
    timeout: 10000,
    headers: {
      "Content-Type": "application/json",
    },
  };

  return request(options, message)
    .then(() => {
      console.log(`[Slack 발송 성공] message=${JSON.stringify(message)}`);
    })
    .catch((e) => {
      console.log(
        `[Slack 발송 실패] message=${JSON.stringify(
          message
        )}, webhook=${webhook}`,
        e
      );
      throw e;
    });
}

function request(options, data) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      res.setEncoding("utf8");
      let responseBody = "";

      res.on("data", (chunk) => {
        responseBody += chunk;
      });

      res.on("end", () => {
        resolve(responseBody);
      });
    });

    req.on("error", (err) => {
      console.error(err);
      reject(err);
    });

    req.write(JSON.stringify(data));
    req.end();
  });
}
