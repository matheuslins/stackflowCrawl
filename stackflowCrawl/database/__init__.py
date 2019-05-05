import certifi

from elasticsearch import Elasticsearch

from stackflowCrawl.settings import ES_HOST, ENVIRONMENT, ES_INDEX


def config_client():
    if ENVIRONMENT == 'dev':
        return Elasticsearch(hosts=ES_HOST, timeout=25)
    return Elasticsearch(hosts=ES_HOST, use_ssl=True, ca_certs=certifi.where(), timeout=25)


if __name__ == '__main__':
    client = config_client()
    client.indices.create(index=ES_INDEX, ignore=400)
