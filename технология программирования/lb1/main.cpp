#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cmath>

// проверка на вещественное число
bool is_double(const std::string& s) {
    std::string::size_type sz;
    try {
        std::stod(s, &sz);
    } catch (...) {
        return false;
    }
    return sz == s.size();
}


double x1, x2;

// вычесление корней
int MatchF(double a, double b, double c) {
    std::cout << "A: " << a << " B: " << b << " C: " << a << std::endl;
    double d = b * b - 4 * a * c;
    std::cout << "Дискриминант: " << d << std::endl;
    if (d > 0) {
       x1 = (-b + sqrt(d)) / (2 * a);
       x2 = (-b - sqrt(d)) / (2 * a);
       return 0;
    } else if (d < 0) {
        x1 = 0;
        x2 = 0;
        return 0;
    } else if (d == 0) {
        x1 = -b / (2 * a);
        return 0;
    } else {
        return 0;
    }
    return 0;
}


int main() {
    // инцилизация и записывание данных в переменные a, b, c;
    //------------------------------------------------------------------------------------------------------------------
    std::string a, b, c;
    std::cout << "введите число A для решение квадратного уравнения: " ;
    std::cin >> a;
    if (is_double(a)) {
        std::cout << "Введено число A для решение квадратного уравнения: " << a << std::endl;
        double number = std::stod(a);
    } else {
        std::cout << "Ошибка: Введена не вещественная строка. Разрешены только числа и вкачестве инкрементов для дробных чисел использовать символ '.' " << std::endl;
        return 0;
    }

    std::cout << "введите число B для решение квадратного уравнения: ";
    std::cin >> b;


    if (is_double(b)) {
        std::cout << "Введено число B для решение квадратного уравнения: " << b << std::endl;
        double number = std::stod(b);
    } else {
        std::cout << "Ошибка: Введена не вещественная строка. Разрешены только числа и вкачестве инкрементов для дробных чисел использовать символ '.' " << std::endl;
        return 0;
    }

    std::cout << "введите число C для решение квадратного уравнения: ";
    std::cin >> c;

    if (is_double(c)) {
        std::cout << "Введено число C для решение квадратного уравнения: " << c << std::endl;
        double number = std::stod(c);
    } else {
        std::cout << "Ошибка: Введена не вещественная строка. Разрешены только числа и вкачестве инкрементов для дробных чисел использовать символ '.' " << std::endl;
        return 0;
    }

    //------------------------------------------------------------------------------------------------------------------
    MatchF(std::stod(a), std::stod(b), std::stod(c));
    if (x1 == 0 && x2 == 0) {
        std::cout << "Корней нет" << std::endl;
        return 0;
    }else if (x1 != 0 && x2 != 0) {
        std::cout << "Корень 1: " <<  x1 <<std::endl;
        std::cout << "Корень 2: " << x2 << std::endl;
    }else if (x1 != 0 && x2 == 0) {
        std::cout << "Корень: " << x2 << std::endl;
    }
    return 0;
}