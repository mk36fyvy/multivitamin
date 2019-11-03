#include <algorithm>
#include <iostream>
#include <set>
#include <stdlib.h>

using namespace std;

struct node {
  string person;
  set<node*> friends;
  node(string p_) : person(p_) {};
  node(string p_, set<node*> f_) : person(p_), friends(f_) {};
  void print() {
    cout<<person<<" ("<<this<<") knows: { ";
    for(auto f : friends)
      cout<<f->person<<" ";
    cout<<"}\n";
  }
};

class graph {
  private:
    set<node*> g;
  public:
    void addNode(string p_) {
      node* n = new node(p_);
      g.insert(n);
    }
    void addEdge(string p1_, string p2_) {
      node* n1 = NULL, *n2 = NULL;
      for(auto p : g) {
        if(p->person == p1_) { n1 = p; }
        else if(p->person == p2_) { n2 = p; }
      }
      if(n1 && n2)
        n1->friends.insert(n2), n2->friends.insert(n1);
    }
    set<node*> getUniverse() {
      return g;
    }
    void print() {
      for(auto p : g)
        (*p).print();
    }
};

void set_print(set<node*> s) {
  cout<<"[ ";
  for(auto p : s)
    cout<<p->person<<" ";
  cout<<"]\n";
}

set<node*> set_union(set<node*> a, set<node*> b) {
  set<node*> c;
  set_union(a.begin(), a.end(), b.begin(), b.end(), inserter(c, c.end()) );
  return c;
}

set<node*> set_intersection(set<node*> a, set<node*> b) {
  set<node*> c;
  set_intersection(a.begin(), a.end(), b.begin(), b.end(), inserter(c, c.end()));
  return c;
}

//note, set_difference is the relative compliment on input set a//
set<node*> set_difference(set<node*> a, set<node*> b) {
  set<node*> c;
  set_difference(a.begin(), a.end(), b.begin(), b.end(), inserter(c, c.end()));
  return c;
}

void bronKerbosch(set<node*> R, set<node*> P, set<node*> X) {
  if(P.empty() && X.empty()) {
    cout<<"Clique found: ";
    set_print(R);
  }
  set<node*>::iterator v = P.begin();
  while(!P.empty()  && v!=P.end()){
    set<node*> singleton = { (*v) };
    bronKerbosch(set_union(R,singleton), set_intersection(P,(*v)->friends), set_intersection(X,(*v)->friends));
    P = set_difference(P,singleton);
    X = set_union(X,singleton);
    if(!P.empty())
      v = P.begin();
  }
}

int main() {
  graph g;
  string people[15] = { "Amy", "Jack", "Erin", "Sally", "Sue", "Max", "Jake", "Tom", "Lu", "Joe", "Ryan", "Jess", "Liz", "Ty", "Jay"};
  for(auto p : people)
    g.addNode(p);

  g.addEdge("Erin","Sally");
  g.addEdge("Sally","Sue");
  g.addEdge("Sally","Max");
  g.addEdge("Max","Sue");
  g.addEdge("Sally","Tom");
  g.addEdge("Sally","Jake");
  g.addEdge("Tom","Jake");
  g.addEdge("Tom","Jess");
  g.addEdge("Tom","Lu");
  g.addEdge("Tom","Ryan");
  g.addEdge("Jess","Jake");
  g.addEdge("Jess","Lu");
  g.addEdge("Jess","Ryan");
  g.addEdge("Lu","Ryan");
  g.addEdge("Lu","Jake");
  g.addEdge("Lu","Joe");
  g.addEdge("Ryan","Jake");
  g.addEdge("Liz","Jay");
  g.addEdge("Liz","Ty");
  g.addEdge("Ty","Jay");
  g.addEdge("Amy","Erin");
  g.addEdge("Amy","Jack");
  g.addEdge("Erin","Jack");
  set<node*> R,P,X;
  P = g.getUniverse();
  bronKerbosch(R,P,X);
  return 0;
}
