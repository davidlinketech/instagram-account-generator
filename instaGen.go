package main

import(
	"fmt"
	"net/url"
	//"strconv"
	"strings"
	//"bytes"
	"compress/gzip"
	"io/ioutil"

	"github.com/davidlinketech/cclient"
	http "github.com/davidlinketech/fhttp"
	utls "github.com/Carcraftz/utls"
)

var client, _ = cclient.NewClient(utls.HelloChrome_100,"",true,6) //empty string = proxy	

func getCookieStr(targetUrl string) string {
	parsed,_ := url.Parse(targetUrl)
	cookie := client.Jar.Cookies(parsed)
	cookieString := ""
	for _, c := range cookie {
		cookieString += c.Name + "=" + c.Value + "; "
	}
	cookieString = cookieString[:len(cookieString)-2]
	return cookieString
}

func main(){
	ioutil.ReadFile("files/proxies.txt")
}