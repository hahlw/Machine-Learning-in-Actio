/*
 * @lc app=leetcode.cn id=328 lang=cpp
 *
 * [328] 奇偶链表
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
    ListNode* oddEvenList(ListNode* head) {
        if(!head||!head->next)return head;
        ListNode*cur=head,*fa=head,*lo=head;
        while(fa->next&&fa->next->next){
            lo=fa->next;
            fa=fa->next->next;
            lo->next=NULL;
            ListNode*node=fa->next;
            fa->next=cur->next;
            cur->next=fa;
            lo->next=node;
            cout<<lo->val;
            fa=lo;
            cur=cur->next;
        }
        return head;
    }
};

