import http from "k6/http";
import { check } from "k6";

const BASE_URL = "http://127.0.0.1:8000";
const TOTAL_LINKS = 1000000;
const HOT_LINKS_PERCENT = 0.1;
const HOT_TRAFFIC_PERCENT = 0.9;
const HOT_LINK_COUNT = Math.floor(TOTAL_LINKS * HOT_LINKS_PERCENT);

const BASE62_ALPHABET =
  "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

const SHARD_BITS = 14;

const base62Encode = (number) => {
  if (number == 0) {
    return BASE62_ALPHABET[0];
  }

  const base = BASE62_ALPHABET.length;
  let chars = [];

  while (number > 0) {
    const remainder = number % base;
    chars.push(BASE62_ALPHABET[remainder]);
    number = Math.floor(number / base);
  }

  return chars.reverse().join("");
};

const randomInt = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const chooseLinkId = () => {
  const chooseHot = Math.random() < HOT_TRAFFIC_PERCENT;

  if (chooseHot) {
    return randomInt(1, HOT_LINK_COUNT);
  }

  return randomInt(HOT_LINK_COUNT + 1, TOTAL_LINKS);
};

const chooseShardId = () => {
  return 1;
};

// TODO: confirm the correct options to use
export const options = {
  scenarios: {
    redirects: {
      executor: "ramping-arrival-rate",
      startRate: 100,
      timeUnit: "1s",
      preAllocatedVUs: 500,
      maxVUs: 5000,
      stages: [
        { duration: "1m", target: 100 },
        { duration: "1m", target: 500 },
        { duration: "1m", target: 1000 },
        { duration: "1m", target: 2000 },
        { duration: "1m", target: 5000 },
        { duration: "1m", target: 10000 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

export default function () {
  const sequence = chooseLinkId();
  const shardId = chooseShardId();
  const uniqueId = (sequence << SHARD_BITS) | shardId;
  const shortId = base62Encode(uniqueId);

  const res = http.get(`${BASE_URL}/links/${shortId}`, {
    redirects: 0,
  });

  check(res, {
    "status is 302": (r) => r.status === 302,
  });
}
