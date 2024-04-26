#include "curl/curl.h"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct curl_slist *headers;
string momo_link = "";
const int count = 100;
CURL *curls[count] = {0};
bool last = false;
static int success_cnt = 0;

static size_t cb(char *d, size_t n, size_t l, void *p)
{
    (void)d;
    (void)p;
    return n * l;
}

int curl_multi(vector<vector<string>> &ip_pass)
{
    CURLM *curlm = curl_multi_init();
    for (int i = 0; i < count; ++i)
    {
        CURL *curl = NULL;
        if (curls[i] == NULL)
        {
            curl = curl_easy_init();
            curls[i] = curl;
        }
        else
        {
            curl = curls[i];
        }

        vector<string> ip = ip_pass[i % ip_pass.size()];
        string ip_link = ip[0];
        string ip_pass = ip[1];
        curl_easy_setopt(curl, CURLOPT_PROXY, ip_link.c_str());
        if (ip_pass != "")
        {
            curl_easy_setopt(curl, CURLOPT_PROXYUSERPWD, ip_pass.c_str());
        }
        curl_easy_setopt(curl, CURLOPT_BUFFERSIZE, 102400L);
        curl_easy_setopt(curl, CURLOPT_URL, momo_link.c_str());
        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0");
        curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 50L);
        curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, (long)CURL_HTTP_VERSION_2TLS);
        curl_easy_setopt(curl, CURLOPT_ACCEPT_ENCODING, "");
        curl_easy_setopt(curl, CURLOPT_FTP_SKIP_PASV_IP, 1L);
        curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1L);
        // 不输出网页
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, cb);
        // 在屏幕打印请求连接过程和返回http数据
        // curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
        // 设置连接超时
        curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 10);

        curl_multi_add_handle(curlm, curl);
    }

    int running_handlers = 0;
    do
    {
        int numfds = 0;
        int res = curl_multi_wait(curlm, NULL, 0, 15000, &numfds);
        if (res != CURLM_OK)
        {
            fprintf(stderr, "error: curl_multi_wait return %d\n", res);
            return -1;
        }
        curl_multi_perform(curlm, &running_handlers);
    } while (running_handlers > 0);

    int msgs_left;
    CURLMsg *msg;
    while ((msg = curl_multi_info_read(curlm, &msgs_left)))
    {
        if (msg->msg == CURLMSG_DONE)
        {
            int http_status_code = 0;
            curl_easy_getinfo(msg->easy_handle, CURLINFO_RESPONSE_CODE, &http_status_code);
            const char *effective_url = NULL;
            curl_easy_getinfo(msg->easy_handle, CURLINFO_EFFECTIVE_URL, &effective_url);
            printf("status:%s\n", curl_easy_strerror(msg->data.result));
            if (msg->data.result == 0)
            {
                ++success_cnt;
            }
            cout << "成功次数: " << success_cnt << endl;

            curl_multi_remove_handle(curlm, msg->easy_handle);
            if (last)
            {
                curl_easy_cleanup(msg->easy_handle);
                msg->easy_handle = NULL;
                curl_slist_free_all(headers);
                headers = NULL;
            }
        }
    }

    curl_multi_cleanup(curlm);

    return 0;
}

int main(int argc, char *argv[])
{
    ifstream in("momo_link.txt");
    if (!in.is_open())
    {
        cout << "Error opening file momo_link.txt";
        exit(1);
    }
    getline(in, momo_link);
    in.close();
    // headers
    headers = NULL;
    headers = curl_slist_append(headers, "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8");
    headers = curl_slist_append(headers, "Accept-Language: en-US,en;q=0.7,zh;q=0.3");
    headers = curl_slist_append(headers, "Accept-Encoding: gzip, deflate, br");
    headers = curl_slist_append(headers, "Connection: keep-alive");
    // headers = curl_slist_append(headers, "Cookie: Hm_lvt_8d4c70ef9b50f1ed364481083d6a8636=1713950649,1714091342; PHPSESSID=b71f97214acbe793729773fe90c44671; Hm_lpvt_8d4c70ef9b50f1ed364481083d6a8636=1714091345");
    headers = curl_slist_append(headers, "Upgrade-Insecure-Requests: 1");
    headers = curl_slist_append(headers, "Sec-Fetch-Dest: document");
    headers = curl_slist_append(headers, "Sec-Fetch-Mode: navigate");
    headers = curl_slist_append(headers, "Sec-Fetch-Site: none");
    headers = curl_slist_append(headers, "Sec-Fetch-User: ?1");
    headers = curl_slist_append(headers, "TE: trailers");

    string line;
    ifstream in1("ip.txt");
    if (!in1.is_open())
    {
        cout << "Error opening file";
        exit(1);
    }
    vector<vector<string>> ip_pass;
    int line_get_cnt = 0;
    while (!in1.eof())
    {
        getline(in1, line);
        cout << "read line: " << ++line_get_cnt << endl;
        vector<string> ip;
        if (line.find(' ') != string::npos)
        {
            // cout << line.substr(line.find(' ') + 1) << endl;
            ip.push_back(line.substr(0, line.find(' ')));
            ip.push_back(line.substr(line.find(' ') + 1));
        }
        else
        {
            ip.push_back(line);
            ip.push_back("");
        }
        ip_pass.push_back(ip);
        if (ip_pass.size() == count)
        {
            curl_multi(ip_pass);
            ip_pass.clear();
        }
    }
    last = true;
    curl_multi(ip_pass);

    return 0;
}