import os

def update_portal():
    with open('portal.html', 'r', encoding='utf-8') as f:
        content = f.read()

    old_str = '<a href="index.html" class="text-amber-900 bg-amber-50 px-2.5 py-0.5 rounded-lg border border-amber-200 hover:bg-amber-100 font-bold flex items-center gap-1 transition text-[11px] sm:text-xs">'
    new_str = '''<a href="/future/portal" class="text-white bg-gradient-to-r from-amber-500 to-amber-600 px-3 py-1 rounded-lg font-black flex items-center gap-1.5 shadow-sm hover:from-amber-600 hover:to-amber-700 transition animate-pulse text-[11px] sm:text-xs">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> ✨ استعراض الوضع المستقبلي
                </a>
                <span class="text-slate-300">|</span>
                <a href="index.html" class="text-amber-900 bg-amber-50 px-2.5 py-0.5 rounded-lg border border-amber-200 hover:bg-amber-100 font-bold flex items-center gap-1 transition text-[11px] sm:text-xs">'''

    if old_str in content:
        content = content.replace(old_str, new_str, 1)
        with open('portal.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("portal.html updated successfully!")
    else:
        print("old_str not found in portal.html")

if __name__ == '__main__':
    update_portal()
