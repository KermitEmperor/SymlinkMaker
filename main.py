from customtkinter import *
from tkinter import messagebox
import os
import ctypes

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main() -> None:
    root = CTk()
    root.title("Symbolic Link Creator")
    root.geometry("490x150")
    root.resizable(False, False)

    targetFolder = Variable(value="Select Where the Symlink will be placed")
    originalFolder = Variable(value="Select Where the Symlink will refer to")

    parameters = {
        "File": "/H",
        "Folder": "/D",
        "Directory Junction": "/J",
    }

    def getOriginal() -> None:
        parameter = parameters[menu.get()]
        if parameter in {"/D", "/J"}:
            originalFolder.set(str(filedialog.askdirectory(initialdir="/", title="Select Where the Symlink will refer to")))
        if parameter in "/H":
            originalFolder.set(str(filedialog.askopenfilename(initialdir="/", title="Select Where the Symlink will refer to")))

    def generate() -> None:
        parameter = parameters[menu.get()]
        Target = targetFolder.get()
        Original = originalFolder.get()
        print(Target, Original , parameter)
        if not os.path.exists(Original):
            messagebox.showerror("Incorrect Original file/folder", "Selected original folder/file is incorrect")
            return
        if not os.path.exists(Target):
            messagebox.showerror("Incorrect Symlink location", "Selected folder for Symlink location is incorrect")
            return
        NewName = str(Original).split("/")[-1]
        Target = Target+"\\"+NewName
        
        def quote(string: str) -> str:
            return "\""+string+"\""
        
        
        argss = " ".join(["mklink", quote(Target), quote(Original), parameter])
        try: 
            os.system(argss)
            messagebox.showinfo("Symlink", "The symlink may or not be done")
        except: messagebox.showerror("Something Happened", "During the symlink setup, something went wrong")



    CTkLabel(root, text="Place symlink here:").place(relx=0.02, rely= 0.03)
    CTkEntry(root, textvariable=targetFolder, width=325).place(relx=0.25, rely= 0.03)
    CTkButton(root, text="[...]", width= 30, command=lambda: targetFolder.set(str(filedialog.askdirectory(initialdir="/", title="Select Where the Symlink will be placed")))).place(relx=0.92, rely= 0.03)

    CTkLabel(root, text="Original file/folder:").place(relx=0.02, rely= 0.24)
    CTkEntry(root, textvariable=originalFolder, width=325).place(relx=0.25, rely= 0.24)
    CTkButton(root, text="[...]", width= 30, command=getOriginal).place(relx=0.92, rely= 0.24)

    CTkLabel(root, text="Choose Type:").place(relx=0.02, rely= 0.45)
    menu = CTkOptionMenu(root, values=["File", "Folder", "Directory Junction"])
    menu.place(relx=0.25, rely= 0.45)

    CTkButton(root, text="Generate Symlink", command=generate).place(relx=0.375, rely = 0.8)


    root.mainloop()
    
if __name__ == "__main__":
    if is_admin():
        main()
    else:
        messagebox.showerror("Missing rights!", "\"mklink\" requires administrator rights (run this as admin)")
        quit()
    