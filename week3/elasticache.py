import redis
from get_env import get_elasticache
import boto3

class ElastiCache:
    def __init__(self):
        # session = boto3.Session(profile_name='pyo')
        # boto_client = session.client('elasticache')
        # response = boto_client.describe_cache_clusters(CacheClusterId='pyo-redis')
        # endpoint = response['CacheClusters'][0]['ConfigurationEndpoint']
        host, port = get_elasticache()
        self.client = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key)

    def keys(self, pattern):
        return self.client.keys(pattern)


def main():
    cache = ElastiCache()
    cache.set('pyo', 'ok')
    print(cache.get('pyo'))
main()
