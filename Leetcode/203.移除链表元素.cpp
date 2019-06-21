/*
 * @lc app=leetcode.cn id=203 lang=cpp
 *
 * [203] 移除链表元素
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
    ListNode* removeElements(ListNode* head, int val) {
        if(!head)return head;
        ListNode*h=new ListNode(-1);
        h->next=head;
        ListNode*pre=h,*cur=h->next;
        while(cur){
            if(cur->val==val){
                pre->next=pre->next->next;
                cur=pre;
                cur=pre->next;
            }
            else{
                pre=pre->next;
                cur=cur->next;
            }
        }
        return h->next;
    }
};

