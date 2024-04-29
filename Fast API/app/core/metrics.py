# from prometheus_client import Counter, Gauge, Histogram, Summary
# from redis.asyncio import Redis
from tortoise.backends.base.client import BaseDBAsyncClient

from app import crud
from app.core.configs import settings


class HTTPMetrics:
    def __init__(
        self,
        namespace: str = "",
        subsystem: str = "",
        latency_highr_buckets: list[float] | None = None,
        latency_lowr_buckets: list[float] | None = None,
    ):
        self.namespace = namespace
        self.subsystem = subsystem
        self.latency_highr_buckets = latency_highr_buckets or [
            0.01,
            0.025,
            0.05,
            0.075,
            0.1,
            0.25,
            0.5,
            0.75,
            1.0,
            1.5,
            2.0,
            2.5,
            3.0,
            3.5,
            4.0,
            4.5,
            5.0,
            7.5,
            10.0,
            30.0,
            60.0,
            float("inf"),
        ]
        self.latency_lowr_buckets = latency_lowr_buckets or [0.1, 0.5, 1.0, float("inf")]
        if (
            float("inf") not in self.latency_highr_buckets
            or float("inf") not in self.latency_lowr_buckets
        ):
            raise ValueError(
                "latency_highr_buckets and latency_lowr_buckets should have infinity"
            )

        self.http_request_size_bytes = Summary(
            name="http_request_size_bytes",
            documentation=(
                "Content length of incoming requests by handler. "
                "Only value of header is respected. Otherwise ignored. "
                "No percentile calculated. "
            ),
            labelnames=("handler",),
            namespace=namespace,
            subsystem=subsystem,
        )
        self.http_response_size_bytes = Summary(
            name="http_response_size_bytes",
            documentation=(
                "Content length of outgoing responses by handler. "
                "Only value of header is respected. Otherwise ignored. "
                "No percentile calculated. "
            ),
            labelnames=("handler",),
            namespace=namespace,
            subsystem=subsystem,
        )
        self.http_request_duration_highr_seconds = Histogram(
            name="http_request_duration_highr_seconds",
            documentation=(
                "Latency with many buckets but no API specific labels. "
                "Made for more accurate percentile calculations. "
            ),
            buckets=self.latency_highr_buckets,
            namespace=namespace,
            subsystem=subsystem,
        )
        self.http_request_duration_seconds = Histogram(
            name="http_request_duration_seconds",
            documentation=(
                "Latency with only few buckets by handler. "
                "Made to be only used if aggregation by handler is important. "
            ),
            buckets=self.latency_lowr_buckets,
            labelnames=("handler",),
            namespace=namespace,
            subsystem=subsystem,
        )

    def update(
        self,
        method: str,
        status_code: int,
        handler: str,
        duration: float,
        request_size: int,
        response_size: int,
    ) -> None:
        self.http_requests_total.labels(method, status_code, handler).inc()
        self.http_request_size_bytes.labels(handler).observe(request_size)
        self.http_response_size_bytes.labels(handler).observe(response_size)
        self.http_request_duration_highr_seconds.observe(duration)
        self.http_request_duration_seconds.labels(handler).observe(duration)


class ExternalResourceMetrics:
    def __init__(
        self,
        namespace: str = "",
        subsystem: str = "",
    ):
        self.participants_in_group_total = Gauge(
            name="participants_in_group_total",
            documentation="Total participants in Telegram group",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.participants_in_channel_total = Gauge(
            name="participants_in_channel_total",
            documentation="Total participants in Telegram channel",
            namespace=namespace,
            subsystem=subsystem,
        )

        self.participants_total = Gauge(
            name="participants_total",
            documentation="Total participants",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.participants_verified_twitter_account_total = Gauge(
            name="participants_verified_twitter_account_total",
            documentation="Total participants with verified Twitter account",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.participants_verified_twitter_follower_total = Gauge(
            name="participants_verified_twitter_follower_total",
            documentation="Total participants with verfied Twitter account",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.participants_completed_total = Gauge(
            name="participants_completed_total",
            documentation="Total participants whom completed all tasks",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.twitter_follower_total = Gauge(
            name="twitter_follower_total",
            documentation="Total Twitter followers",
            namespace=namespace,
            subsystem=subsystem,
        )
        self.youtube_subscriber_total = Gauge(
            name="youtube_subscriber_total",
            documentation="Total Youtube subscribers",
            namespace=namespace,
            subsystem=subsystem,
        )

    async def fetch_and_update(self, db: BaseDBAsyncClient, redis: Redis) -> None:
        participant_total_members = await crud.participant.get_total_members(db)
        self.twitter_follower_total.set(await crud.twitter_account.count_followers(db))
        self.youtube_subscriber_total.set(
            await crud.dynamic_configs.get_total_youtube_subscribers(redis)
        )
        self.participants_total.set(participant_total_members["total_participants"])
        self.participants_in_group_total.set(
            participant_total_members["total_group_members"]
        )
        self.participants_in_channel_total.set(
            participant_total_members["total_channel_members"]
        )
        self.participants_verified_twitter_account_total.set(
            participant_total_members["total_verified_twitter_accounts"]
        )
        self.participants_verified_twitter_follower_total.set(
            participant_total_members["total_verified_twitter_followers"]
        )
        self.participants_completed_total.set(
            participant_total_members["total_completed_participants"]
        )


http_metrics = HTTPMetrics(
    settings.METRICS_HTTP_NAMESPACE, settings.METRICS_HTTP_SUBSYSTEM
)
external_resource_metrics = ExternalResourceMetrics(
    settings.METRICS_EXTERNAL_RESOURCE_NAMESPACE,
    settings.METRICS_EXTERNAL_RESOURCE_SUBSYSTEM,
)
