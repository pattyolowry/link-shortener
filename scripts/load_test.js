import http from "k6/http";
import { check } from "k6";

const BASE_URL = "http://127.0.0.1:8000";
const TOTAL_LINKS = 1000000;
const HOT_LINKS_PERCENT = 0.1;
const HOT_TRAFFIC_PERCENT = 0.9;
const HOT_LINK_COUNT = Math.floor(TOTAL_LINKS * HOT_LINKS_PERCENT);

const BASE62_ALPHABET =
  "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

const SHARD_BITS = 14n;
const SEQUENCE_BITS = 50n;

const MAX_SHARD_ID = (1n << SHARD_BITS) - 1n;
const MAX_SEQUENCE = (1n << SEQUENCE_BITS) - 1n;

const base62Encode = (number) => {
  if (number == 0n) {
    return BASE62_ALPHABET[0];
  }

  const base = 62n;
  let chars = [];

  while (number > 0n) {
    const remainder = number % base;
    chars.push(BASE62_ALPHABET[remainder]);
    number = number / base;
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
      startRate: 400,
      timeUnit: "1s",
      preAllocatedVUs: 200,
      maxVUs: 2000,
      stages: [{ duration: "300s", target: 400 }],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<100"],
  },
};

export default function () {
  const sequence = chooseLinkId();
  const shardId = chooseShardId();
  const uniqueId = (BigInt(sequence) << SHARD_BITS) | BigInt(shardId);
  const shortId = base62Encode(uniqueId);
  if (!shortId) {
    throw new Error(
      `Generated empty shortId for sequence=${sequence}, shard=${shardId}, uniqueId=${uniqueId}`,
    );
  }

  const res = http.get(`${BASE_URL}/links/${shortId}`, {
    redirects: 0,
    tags: {
      name: "GET /links/{short_id}",
    },
  });

  check(res, {
    "status is 302": (r) => r.status === 302,
  });
}
