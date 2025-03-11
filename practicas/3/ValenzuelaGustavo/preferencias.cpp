#include <iostream>
#include <string>
#include <set>

int main(){
    std::set<std::string> lenguajes = {
        "C", "C++", "Python", "Java", "JavaScript", "Ruby", "Perl", "PHP", "Assembly", 
        "Pascal", "Kotlin", "Objective-C", "Swift", "Rust", "Go", "TypeScript", "Scala", 
        "Lua", "Haskell", "Dart", "R"
    };
    
    std::string lenguaje = "";
    std::cout<<"¡Hola! ¿Cuál es tu lenguaje de programación favorito?"<<"\n";
    std::cin>>lenguaje;

    if(lenguajes.find(lenguaje) != lenguajes.end())
        std::cout<<lenguaje<<" es un lenguaje muy god :D"<<"\n";
    else{
        std::cout<<"Wow ¡No conocía ese lenguaje! :O" <<"\n";
    }
    return 0;
}