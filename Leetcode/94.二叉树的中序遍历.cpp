/*
 * @lc app=leetcode.cn id=94 lang=cpp
 *
 * [94] 二叉树的中序遍历
 */
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        stack<TreeNode*>s;
        vector<int>res;
        if(!root)return res;
        // s.push(root);
        TreeNode*h=root;
        while(h||!s.empty()){
            while(h){
                s.push(h);
                h=h->left;
            }
            if(!s.empty()){
                TreeNode*node=s.top();
                res.push_back(node->val);
                h=node->right;
                s.pop();
            }
        }
        return res;
    }
};

