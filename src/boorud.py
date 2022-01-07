import argparse
import safebooru as sb

def main():
    def init_tags(tags):
        return (tags.strip()).replace(', ', '+').replace(' ', '_').lower()

    args = parser.parse_args()
    post_limit = args.posts
    tags = ''

    if args.tags:
        tags = init_tags(args.tags)
        # print(tags)
        client = sb.safebooru(limit=post_limit, tags=tags)
        post = client.get_posts()
        if post:
            print(f'Found {len(post)} images.')
            client.save_images()
        else:
            print('Uh oh! Can\'t find any posts related to your input tags')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloading images from safebooru.', add_help=True)
    parser.add_argument('--tags', required=True, type=str, help='Tags to search for (multipletags go between \'\' separated by ,)')
    parser.add_argument('--posts', type=int, default=100, help='Number of posts to download')
    main()
