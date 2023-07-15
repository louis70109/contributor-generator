import argparse
import requests
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="LINE Notify access_token")
    parser.add_argument("--owner", required=True, help="Github repo owner, ex: louis70109")
    parser.add_argument("--repo", required=True, help="Github Repo name, ex: lotify")
    args = parser.parse_args()
    
    
    # 定義GraphQL請求
    query = """
    {
      repository(owner: "<OWNER>", name: "<REPO>") {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100) {
                edges {
                  node {
                    author {
                      user {
                        login
                        avatarUrl
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    # 填入你的GitHub用戶名和存儲庫名稱
    owner = args.owner
    repo = args.repo

    # 替換GraphQL請求中的佔位符
    query = query.replace("<OWNER>", owner).replace("<REPO>", repo)

    # 發送POST請求
    url = "https://api.github.com/graphql"
    git_token = args.token
    headers = {
        "Authorization": f"Bearer {git_token}"
    }
    response = requests.post(url, headers=headers, json={"query": query})

    # 解析響應
    data = json.loads(response.text)

    # 獲取貢獻者列表
    contributors, avatars = [], []
    edges = data["data"]["repository"]["defaultBranchRef"]["target"]["history"]["edges"]
    for edge in edges:
        login = edge["node"]["author"]["user"]["login"]
        avatar = edge["node"]["author"]["user"]["avatarUrl"]
        if login not in contributors:
            contributors.append(login)
        if avatar not in avatars:
            avatars.append(avatar)

    # 將貢獻者列表轉換為Markdown格式

    print(contributors)

    markdown=''
    for idx in range(len(contributors)):
      markdown += f'<img src="{avatars[idx]}" alt="{contributors[idx]}" style="max-width: 30px; border-radius: 50%;">'

    # 打印Markdown格式
    print(markdown)

    # 讀取README文件的內容
    with open("README.md", "r") as file:
        readme_content = file.read()

    # 在README文件中找到"# Contributor"標題的位置
    contributor_title_index = readme_content.index("## Contributor")

    # 取得"# Contributor"標題後的內容
    contributor_content = readme_content[contributor_title_index:]

    # 替換"# Contributor"標題後的內容為帶有圖片的貢獻者清單
    new_readme_content = readme_content.replace(contributor_content, f"## Contributor\n\n{markdown}")

    # 將更新後的內容寫入README文件
    with open("README.md", "w") as file:
        file.write(new_readme_content)