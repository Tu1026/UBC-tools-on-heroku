#include <cmath> 
/**
 * @file avltree.cpp
 * Definitions of the binary tree functions you'll be writing for this lab.
 * You'll need to modify this file. IMPORTANT: read avltree.h to understand
 * what to do in this lab.
 */

template <class K, class V>
V AVLTree<K, V>::find(const K& key) const
{
    return find(root, key);
}

template <class K, class V>
V AVLTree<K, V>::find(Node* subtree, const K& key) const
{
    if (subtree == NULL)
        return V();
    else if (key == subtree->key)
        return subtree->value;
    else {
        if (key < subtree->key)
            return find(subtree->left, key);
        else
            return find(subtree->right, key);
    }
}

template <class K, class V>
void AVLTree<K, V>::insert(const K & key, const V & value)
{
    insert(root, key, value);
}

template <class K, class V>
void AVLTree<K, V>::insert(Node*& subtree, const K& key, const V& value)
{
    /** 
     * TODO: your code here. Make sure the following cases are included:
     * Case 1: subtree is NULL
     * Case 2: (key, value) pair should be inserted into left subtree
     * Case 3: (key, value) pair should be inserted into right subtree
     */
    if (subtree == NULL)
        subtree = new Node(key, value);
    else {
        if (key < subtree->key) {
            insert(subtree->left, key, value);
        } else {
            insert(subtree->right, key, value);
        }
    }
  

    // Rebalance tree after insertion (don't remove this)
    rebalance(subtree);
}

template <class K, class V>
void AVLTree<K, V>::updateHeight(Node* node)
{
    // int left = 0;
    // int right = 0;
    // Node* left_node = node->left;
    // Node* right_node = node->right;

    // while(left_node != NULL) {
    //     left++;
    //     left_node = left_node
    // }

    // while(right_node != NULL){
    //     right++;
    // }
    if (node->left == NULL && node->right != NULL)  {
        node->height = node->right->height + 1;
    } else if (node->right == NULL && node->left != NULL) {
        node->height =  node->left->height + 1;
    } else if (node->right != NULL && node->left != NULL) {
        node->height =  max(node->left->height, node->right->height) + 1;
    } else {
        node->height = 1;
    }
}

template <class K, class V>
void AVLTree<K, V>::rotateLeft(Node*& t)
{
    *_out << __func__ << endl; // Outputs the rotation name (don't remove this)
    

    Node* newSubRoot = t->right;
    t->right = newSubRoot->left;
    newSubRoot->left = t;
    t = newSubRoot;

    updateHeight(t->left);
    updateHeight(t);
    // TODO: update the heights for t->left and t (in that order)
}

template <class K, class V>
void AVLTree<K, V>::rotateRight(Node*& t)
{
    *_out << __func__ << endl; // Outputs the rotation name (don't remove this)

    Node* newSubRoot = t->left;
    t->left = newSubRoot->right;
    newSubRoot->right = t;
    t = newSubRoot;

    updateHeight(t->right);
    updateHeight(t);
    // TODO: your code here
}

template <class K, class V>
void AVLTree<K, V>::rotateLeftRight(Node*& t)
{
    *_out << __func__ << endl; // Outputs the rotation name (don't remove this)

    // TODO: your code here
    Node* left = t->left;
    rotateLeft(left);
    
    // HINT: you should make use of the other functions defined in this file,
    // instead of manually changing the pointers again
}

template <class K, class V>
void AVLTree<K, V>::rotateRightLeft(Node*& t)
{
    *_out << __func__ << endl; // Outputs the rotation name (don't remove this)
    Node* right = t->right;
    rotateLeft(right);
    rotateRight(t);
   // TODO: your code here
}

template <class K, class V>
void AVLTree<K, V>::rebalance(Node*& subtree)
{
    /** 
      * TODO: your code here. Make sure the following cases are included:
      * Cases 1-4: the four cases of tree imbalance as discussed in lecture
      * Case 5: the tree is already balanced. You MUST still correctly update
      * subtree's height 
      */
    int left_score = subtree->left == NULL? 0:subtree->left->height;
    int right_score = subtree->right == NULL? 0:subtree->right->height;

    int score = abs(left_score - right_score);
  
    if (score > 1) {
        if(left_score > right_score) {
            int left_right_score = subtree->left->right == NULL? 0:subtree->left->right->height;
            int left_left_score = subtree->left->left == NULL? 0:subtree->left->left->height;
            if(left_right_score > left_left_score) {
                rotateLeftRight(subtree);
            }
            else {
                rotateRight(subtree);
            }
        }
        else {
            int right_left_score = subtree->right->left == NULL? 0:subtree->right->left->height;
            int right_right_score = subtree->right->right == NULL? 0:subtree->right->right->height;
            if(right_left_score > right_right_score) {
            rotateRightLeft(subtree);
            }

            else {
            rotateLeft(subtree);
            }
        }
    }

    updateHeight(subtree);

}

template <class K, class V>
void AVLTree<K, V>::remove(const K& key)
{
    remove(root, key);
}

template <class K, class V>
void AVLTree<K, V>::remove(Node*& subtree, const K& key)
{
    if (subtree == NULL)
        return;

    if (key < subtree->key) {
        remove(subtree->left, key);
        rebalance(subtree);
    } else if (key > subtree->key) {
        remove(subtree->right, key);
        rebalance(subtree);
    } else {
        /* Reached the node that we need to delete */
        if (subtree->left == NULL && subtree->right == NULL) {
            /* Case 1: Node to remove has no children */
            delete subtree;
            subtree = NULL;
            return;
        } else if (subtree->left != NULL && subtree->right != NULL) {
            /**
             * Case 2: Node to remove has two children
             * TODO: your code here. For testing purposes, you
             * should use the PREDECESSOR.
             */

            
        } else {
            /* Case 3: Node to remove has one child */
            Node* curr = subtree;
            subtree = max(subtree->left, subtree->right);
            delete curr;
        }
        rebalance(subtree);
    }
}
