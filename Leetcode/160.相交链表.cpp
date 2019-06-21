/*
 * @lc app=leetcode.cn id=160 lang=cpp
 *
 * [160] 相交链表
 */

// #include<iostream>
// using namespace std;
// struct ListNode {
//     int val;
//     ListNode *next;
//     ListNode(int x) : val(x), next(NULL) {}
// };

class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        int lenA=0;
        int lenB=0;
        ListNode*ha=headA;
        ListNode*hb=headB;
        while(ha){
            lenA++;
            ha=ha->next;
        }
        while(hb){
            lenB++;
            hb=hb->next;
        }
        ListNode*tmp;
        if(lenB>lenA){
            tmp=headB;
            headB=headA;
            headA=tmp;
        }
        int diff=lenA>=lenB?lenA-lenB:lenB-lenA;
        ha=headA;
        hb=headB;
        while(diff--){
            ha=ha->next;
        }
        while(ha&&hb){
            if(ha==hb)
                return ha;
            else{
                ha=ha->next;
                hb=hb->next;
            }
        }
        return NULL;
    }
};

