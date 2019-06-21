/*
 * @lc app=leetcode.cn id=234 lang=cpp
 *
 * [234] 回文链表
 */
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool isPalindrome(ListNode* head) {
        if(!head||!head->next)return true;
        ListNode*lo=head,*fa=head;
        while(fa->next&&fa->next->next){
            fa=fa->next->next;
            lo=lo->next;
        }
        fa=lo->next;
        lo->next=NULL;
        lo=head;
        ListNode*newfa=new ListNode(-1);
        while(fa){
            ListNode*tmp=fa->next;
            fa->next=newfa->next;
            newfa->next=fa;
            fa=tmp;
        }
        newfa=newfa->next;
        while(lo&&newfa){
            if(lo->val==newfa->val){
                lo=lo->next;
                newfa=newfa->next;
            }
            else
            {
                return false;
            }
            
        }
        if((!lo&&!newfa)||(!lo->next&&!newfa))return true;
        return false;
    }
};

