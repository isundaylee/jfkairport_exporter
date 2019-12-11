import argparse
import time
import logging

import prometheus_client

from jfkairport.collect import *


class Args(argparse.Namespace):
    port: int
    interval: float


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        "main.py", description="JFK airport TSA queue exporter for Prometheus."
    )

    parser.add_argument(
        "--port",
        type=int,
        default=9353,
        help="Port number for the Prometheus exporter to listen on. Default: 9353.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=300.0,
        help="How often (in seconds) to scrape the data. Default: 300.",
    )

    return parser.parse_args(namespace=Args())


gauge_tsa_wait_time = prometheus_client.Gauge(
    "airport_tsa_wait_time_seconds",
    "Airport TSA queue wait time in seconds.",
    ["terminal", "type"],
)


def scrape_data():
    logging.info("Scraping data...")

    for entry in collect_security_wait_times():
        gauge_tsa_wait_time.labels(
            terminal=entry.terminal, type=entry.queue_type.name
        ).set(entry.wait_time_seconds)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    prometheus_client.start_http_server(args.port)
    logging.info(f"Started listening on port {args.port}")

    start = time.time()
    while True:
        scrape_data()
        time.sleep(max(0.0, start + args.interval - time.time()))
        start = max(start + args.interval, time.time())


if __name__ == "__main__":
    main()
