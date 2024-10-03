def parse_file(file_in, file_out):
    with open(file_in, 'r', encoding="utf8") as fin:
        with open(file_out, 'w', encoding="utf8") as fout:
            url = None
            headers = {}
            for line in fin:
                line = line.strip()
                if line.startswith(("GET", "POST", "PUT")):
                    if url is not None:
                        print_request(url, headers, fout)
                    parts = line.split(' ')
                    url = parts[1]
                    headers = {}
                elif line.startswith(("User-Agent", "Pragma", "Cache-control", "Accept", "Accept-Encoding", "Cookie")):
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
            if url is not None:
                print_request(url, headers, fout)