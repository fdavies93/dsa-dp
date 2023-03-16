#include <iostream>
#include <string>

class Node {
    public:
        std::string data;
        Node* next;
        Node(std::string, Node*);
};

Node::Node(std::string data, Node* next) {
    this->data = data;
    this->next = next;
}

int main() {
    Node* node1 = new Node("This is my node.", NULL);
    Node* node2 = new Node("This is another node.", NULL);

    node1->next = node2;

    std::cout << node1->data;
    std::cout << node2->data;
    std::cout << node1->next->data;
    return 1;
}
