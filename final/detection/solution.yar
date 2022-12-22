rule Detect_Nmap_User_Agent {
    meta:
        description = "Detect Nmap User-Agent header"
        author = "kernelmethod"

    strings:
        $ua = "Nmap Scripting Engine; https://nmap.org/book/nse.html"

    condition:
        $ua
}

rule Detect_SQLmap_User_Agent {
    meta:
        description = "Detect SQLmap User-Agent header"
        author = "kernelmethod"

    strings:
        // You don't really need a regex for SQLmap, this is just another way to
        // do this problem.
        $ua = /sqlmap\/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(#.*|) \(https:\/\/sqlmap\.org\)/

    condition:
        $ua
}

rule Detect_SQLi_Attempts {
    meta:
        description = "Detect attempts to perform SQL injection"
        author = "kernelmethod"

    strings:
        $s1 = "%28SELECT%20CONCAT%28CONCAT%28%28CHR"
        $s2 = "%27%20AND%208757%3DCAST%28%28CHR"
        $s3 = "%20FROM%20PG_SLEEP"
        $s4 = "%27%20ORDER%20BY%20"
        $s5 = "%27%20UNION%20ALL%20SELECT%20NULL%2CNULL%2CNULL%2C%28CHR"
        $s6 = "SELECT%20%28CASE%20WHEN%20"
        $s7 = "%27%20UNION%20ALL%20SELECT%20NULL%2CNULL%2CARRAY_AGG%28%28CHR%"

    condition:
        5 of them
}
