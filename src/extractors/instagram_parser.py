thonimport requests
import json

class InstagramParser:
    def __init__(self, post_url, cookies_json, max_depth=5):
        self.post_url = post_url
        self.cookies_json = cookies_json
        self.max_depth = max_depth
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.base_url = 'https://www.instagram.com/graphql/query/'

    def get_post_id(self):
        # Extract post ID from the URL
        post_id = self.post_url.split('/')[-2]
        return post_id

    def scrape_comments(self):
        post_id = self.get_post_id()
        comments = []
        variables = {
            'shortcode': post_id,
            'first': 50
        }
        url = self.base_url
        params = {
            'query_id': '17861898931705474',
            'variables': json.dumps(variables)
        }
        cookies = json.loads(self.cookies_json)
        response = requests.get(url, params=params, headers=self.headers, cookies=cookies)
        
        if response.status_code == 200:
            data = response.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
            comments = [self.parse_comment(comment) for comment in data]
        else:
            print(f"Error: {response.status_code}")
        return comments

    def parse_comment(self, comment_data):
        comment = comment_data['node']
        return {
            'pk': comment['id'],
            'user': {
                'username': comment['owner']['username'],
                'profile_pic_url': comment['owner']['profile_pic_url'],
                'id': comment['owner']['id'],
                'is_verified': comment['owner']['is_verified'],
                'fbid_v2': comment['owner']['fbid_v2']
            },
            'text': comment['text'],
            'created_at': comment['created_at'],
            'comment_like_count': comment['edge_liked_by']['count'],
            'child_comment_count': comment['edge_threaded_comments']['count'],
            'restricted_status': comment.get('restricted_status'),
            'has_translation': comment.get('has_translation', False),
            'has_liked_comment': comment['has_liked_comment'],
            'parent_comment_id': comment.get('parent_comment_id')
        }