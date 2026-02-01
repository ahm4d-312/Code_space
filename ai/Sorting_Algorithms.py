class Sorting_Algorithms:
    def __init__(self):
        self.UNORDERED_LIST=[42,17,8,99,23,56,4,31,65,12,1,78,9,50,28]
    
    @staticmethod
    def is_sorted(lis): # check if the list is already sorted, avoid worst case scenarios in some algorithms
        # ascending and descending order checking
        ascending=True
        descending=True
        for i in range(len(lis)-1):
            if lis[i]>lis[i+1]:
                ascending=False
            elif lis[i]<lis[i+1]:
                descending=False
        return ascending or descending
        
    @staticmethod
    def __partition(lis,first,last):
        pivot=lis[first]
        i=first
        j=last+1

        while True:
            while True:
                i+=1
                if i >=last or lis[i] >=pivot:
                    break
            
            while True:
                j-=1
                if j<=first or lis[j] <=pivot:
                    break

            if i >=j:
                break
            lis[i],lis[j]=lis[j],lis[i]
        lis[j],lis[first]=lis[first],lis[j]
        return j

    def quick_sort(self,lis=None,first=None,last=None,check_sorted=True):
        if lis is None:  # you can add and sort any list, if no list is passed the UNORDERED_LIST attribute will be sorted
            lis=self.UNORDERED_LIST.copy()
        
        if check_sorted:# on the first run check if the list is already sorted
            if Sorting_Algorithms.is_sorted(lis):
                return lis
            check_sorted=False
            
        if first is None and last is None: # so when you need to call it you just pass the list name, no need to pass first and last
            first,last=0,len(lis)-1
        
        if first < last:
            pivot=Sorting_Algorithms.__partition(lis,first,last)
            self.quick_sort(lis,first,pivot-1,check_sorted)
            self.quick_sort(lis,pivot+1,last,check_sorted)
        return lis

    @staticmethod
    def __merge(left,right):
        merged_list=[]
        i,j=0,0
        while i < len(left)and j < len(right):
            if left[i]<right[j]:
                merged_list.append(left[i])
                i+=1
            else:
                merged_list.append(right[j])
                j+=1
        merged_list.extend(left[i:])
        merged_list.extend(right[j:])
        return merged_list

    def merge_sort(self, lis=None, check_sorted=True):
        if lis is None:  # you can add and sort any list, if no list is passed the UNORDERED_LIST attribute will be sorted
            lis=self.UNORDERED_LIST.copy()
        if check_sorted:# on the first run check if the list is already sorted
            if Sorting_Algorithms.is_sorted(lis):
                return lis
            check_sorted=False
        if len(lis)<=1:
            return lis
        mid=len(lis)//2
        left=lis[:mid]
        right=lis[mid:]
        sorted_left=self.merge_sort(left,check_sorted)
        sorted_right=self.merge_sort(right,check_sorted)

        return Sorting_Algorithms.__merge(sorted_left,sorted_right)

    def bubble_sort(self,lis=None):
        if lis is None: # you can add and sort any list, if no list is passed the UNORDERED_LIST attribute will be sorted
            lis=self.UNORDERED_LIST.copy() # copy the original unordered list
        
        if Sorting_Algorithms.is_sorted(lis):# on the first run check if the lis is already sorted
            return lis

        for i in range(len(lis)):
            for j in range(0,len(lis)-i-1):
                if lis[j]>lis[j+1]:
                    lis[j],lis[j+1]=lis[j+1],lis[j]
        return lis
    
    def selection_sort(self,lis=None):
        if lis is None:# you can add and sort any list, if no list is passed the UNORDERED_LIST attribute will be sorted
            lis=self.UNORDERED_LIST.copy() # copy the original unordered list
        
        if Sorting_Algorithms.is_sorted(lis): # on the first run check if the lis is already sorted
            return lis
        
        for i in range(len(lis) - 1):
            min_index = i               #here we select the first element as mini
            for j in range(i + 1, len(lis)):
                if lis[j] < lis[min_index]:
                    min_index = j
            lis[i], lis[min_index] = lis[min_index], lis[i]
        return lis

    def insertion_sort(self,lis=None):
        if lis is None:# you can add and sort any list, if no list is passed the UNORDERED_LIST attribute will be sorted
            lis=self.UNORDERED_LIST.copy() # copy the original unordered list
        
        if Sorting_Algorithms.is_sorted(lis): # on the first run check if the lis is already sorted
            return lis
        
        for i in range(1,len(lis)):
            key=lis[i]
            j=i-1
            while j>-1 and key<lis[j]:
                lis[j+1]=lis[j]
                j-=1
            lis[j+1]=key
        return lis


def main():
    obj=Sorting_Algorithms() 
    # lis=[3,2,1,-1,2.5] you can define any list and sort it, and pass it as a parameter
    print(f'Original list: {obj.UNORDERED_LIST}\n')
    print(f'Bubble_sort: {obj.bubble_sort()}, is_sorted: {'Yes' if obj.is_sorted(obj.bubble_sort()) else 'No'}')
    print(f'Selection_sort: {obj.selection_sort()}, is_sorted: {'Yes' if obj.is_sorted(obj.selection_sort()) else 'No'}')
    print(f'Insertion_sort: {obj.insertion_sort()}, is_sorted: {'Yes' if obj.is_sorted(obj.insertion_sort()) else 'No'}')
    print(f'Quick_sort: {obj.quick_sort()}, is_sorted: {'Yes' if obj.is_sorted(obj.quick_sort()) else 'No'}')
    print(f'Merge_sort: {obj.merge_sort()}, is_sorted: {'Yes' if obj.is_sorted(obj.merge_sort()) else 'No'}')
    
if __name__=="__main__":
    main()