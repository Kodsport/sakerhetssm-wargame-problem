#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>

#include <iostream>
#include <string>

constexpr auto server_port = 1337;

auto get_server_ip() {
    std::string server_ip {};

    std::cout << "server ip: " << std::flush;
    std::cin >> server_ip;

    return server_ip;
}

auto get_username() {
    std::string username {};

    std::cout << "username: " << std::flush;
    std::cin >> username;

    return username;
}

auto get_password() {
    std::string password {};

    std::cout << "password: " << std::flush;
    std::cin >> password;

    return password;
}

auto issue_server(std::string server_ip, std::string message) {
    auto client = socket(AF_INET, SOCK_STREAM, 0);

    hostent* host = gethostbyname(server_ip.c_str());
    sockaddr_in server_address {};

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(server_port);
    server_address.sin_addr.s_addr = inet_addr(inet_ntoa(*(reinterpret_cast<in_addr *>(*host->h_addr_list))));

    connect(client, reinterpret_cast<sockaddr *>(&server_address), sizeof(server_address));

    send(client, message.c_str(), message.length(), 0);

    char response[256] = {0};

    recv(client, response, sizeof(response), 0);

    close(client);

    return std::string(response);
}

auto get_code(std::string server_ip, std::string username, std::string password) {
    auto message = username + ":" + password + "\n";
    return issue_server(server_ip, message);
}

auto has_flag_access(std::string code) {
    return code == "AUTHENTICATED";
}

auto get_flag(std::string server_ip, std::string username, std::string code) {
    return issue_server(server_ip, code + ":" + username + "\n");
}

auto welcome() {
    std::cout << "Welcome to THE GATE." << std::endl;
    std::cout << "In order to get the ~flag~, we first need to validate your identity." << std::endl;
}

auto authenticate() {
    auto server_ip = get_server_ip();
    auto username = get_username();
    auto password = get_password();

    auto code = get_code(server_ip, username, password);

    if (has_flag_access(code)) {
        auto flag = get_flag(server_ip, username, code);

        std::cout << "Welcome back, " << username << " here is your flag: " << flag << std::endl;
    }
    else {
        std::cout << "Sorry, you don't have flag access." << std::endl;        
    }
}

int main() {
    welcome();    
    authenticate();
}