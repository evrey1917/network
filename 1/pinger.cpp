#include <iostream>
#include <unistd.h>
#include <vector>

int main()
{
    std::vector<const char*> domains = {"yandex.ru", "google.com", "steamcommunity.com", "jut.su", "library.ru", "vk.ru", "vk.com", "kalevala.onegaborg.eu", "mangalib.ru", "kinopoisk.ru"};

    for (int i = 0; i < domains.size(); i++)
    {
        switch(fork())
        {
            case -1 : return -1; break;                                                     // failure
            case 0  : execl("/bin/ping", "ping", domains[i], "-c", "4", NULL); break;       // child
            default : break;                                                                // parent
        }
    }

    return 0;
}