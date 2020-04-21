from elasticsearch import Elasticsearch

from stackflowCrawl.settings import ES_HOST, ES_CLUSTER_PASS, ES_CLUSTER_USER


def config_client():
    return Elasticsearch(
        hosts=ES_HOST, timeout=25, http_auth=(ES_CLUSTER_USER, ES_CLUSTER_PASS)
    )
