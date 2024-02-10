#include <iostream>
#include <fstream>
#include <string>
#include <vector>

std::vector<std::string> tokenize(std::string cin_line)
{
    std::vector<std::string> tokenized_line = {};
    std::string word = "\0";

    for (int i = 0; i < cin_line.size(); i++)
    {
        if (cin_line[i] == ' ' || cin_line[i] == '=' || cin_line[i] == '\n')
        {
            tokenized_line.push_back(word);
            word.erase();
            continue;
        }
        word.push_back(cin_line[i]);
    }

    tokenized_line.push_back(word);

    return tokenized_line;
}

std::vector<std::string> get_important_data(std::string cin_line)
{
    std::vector<std::string> important_data = {}, tokenized_line = tokenize(cin_line);

    if (tokenized_line.size() == 12)
    {
        important_data.push_back(tokenized_line[3]);    // Domain name
        important_data.push_back(tokenized_line[6]);    // Number of appeal
        important_data.push_back(tokenized_line[8]);    // TTL
        important_data.push_back(tokenized_line[10]);   // Time
    }

    return important_data;
}

int main()
{
    std::string prev_line = "\0", now_line, separator = ",", next_row = "\n";
    std::vector<const char*> columns = {"Domain", "Number of appeal", "TTL", "Time"};
    std::vector<std::string> data_to_write;

    std::ofstream myfile;
    myfile.open("ping.csv");

    for (int i = 0; i < columns.size(); i++)
    {
        myfile << columns[i] << separator;
    }
    myfile << next_row;

    while (!std::cin.bad())
    {
        getline(std::cin, now_line);

        if (0 == now_line.compare(prev_line))   // check end of ping work
        {
            break;
        }
        prev_line = now_line;

        data_to_write = get_important_data(now_line);

        if (!data_to_write.empty())
        {
            for (int i = 0; i < data_to_write.size(); i++)
            {
                myfile << data_to_write[i] << separator;
            }
            myfile << next_row;
        }
    }

    myfile.close();
    return 0;
}