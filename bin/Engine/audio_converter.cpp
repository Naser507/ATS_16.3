#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {

    if (argc < 3) {
        std::cout << "Usage: audio_converter <input> <output>" << std::endl;
        return 1;
    }

    std::string input = argv[1];
    std::string output = argv[2];

    // ---------------------------------
    // DUMMY CONVERTER (for now)
    // ---------------------------------
    // Just copies file to simulate conversion
    // Later we replace with ffmpeg/libmp3lame/etc.
    // ---------------------------------

    std::ifstream in(input, std::ios::binary);
    if (!in) {
        std::cerr << "Cannot open input file" << std::endl;
        return 1;
    }

    std::ofstream out(output, std::ios::binary);
    if (!out) {
        std::cerr << "Cannot open output file" << std::endl;
        return 1;
    }

    out << in.rdbuf();

    std::cout << "Conversion simulated successfully" << std::endl;

    return 0;
}