from tkinter import Tk, Radiobutton, IntVar, Label, Button, Entry, Frame, filedialog
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import tkinter

class Fong(object):
    # Базовый конструктор
    def __init__(self):
        self.window = 0
        self.faces = (((0, 0, 3), (3, 0, 3), (3, 3, 3), (0, 3, 3)),  # Все точки перечислены против часовой стрелки
                ((0, 0, 3), (0, 3, 3), (0, 3, 0), (0, 0, 0)),
                ((0, 0, 0), (0, 3, 0), (3, 3, 0), (3, 0, 0)),
                ((3, 0, 0), (3, 3, 0), (3, 3, 3), (3, 0, 3)),
                ((3, 0, 0), (3, 0, 3), (0, 0, 3), (0, 0, 0)),
                ((3, 3, 3), (3, 3, 0), (0, 3, 0), (0, 3, 3)))
        self.eye = np.array([6, 6, 6])
        self.lightPosition = np.array([4.0, 5.0, 5.0, 1.0])
        self.lightColor = (1.0, 1.0, 1.0, 1.0)
        self.point = [0, 0, 0]
        self.ambient = (0.2, 0.2, 0.2, 1)

    def keyPressed(self,bkey, x, y):
        try:
            key = bkey.decode("utf-8")
            if key == chr(27):
                sys.exit()
            if key == 'w':
                self.eye = (self.eye[0], self.eye[1] + 1, self.eye[2])
            if key == 's':
                self.eye = (self.eye[0], self.eye[1] - 1, self.eye[2])
            if key == 'd':
                self.eye = (self.eye[0] + 1, self.eye[1], self.eye[2])
            if key == 'a':
                self.eye = (self.eye[0] - 1, self.eye[1], self.eye[2])
            if key == 'q':
                self.eye = (self.eye[0], self.eye[1], self.eye[2] - 1)
            if key == 'e':
                self.eye = (self.eye[0], self.eye[1], self.eye[2] + 1)
            if key == 'y':
                self.lightPosition = (self.lightPosition[0] - 1, self.lightPosition[1], self.lightPosition[2], self.lightPosition[3])
            if key == 'u':
                self.lightPosition = (self.lightPosition[0] + 1, self.lightPosition[1], self.lightPosition[2], self.lightPosition[3])
            if key == 'h':
                self.lightPosition = (self.lightPosition[0], self.lightPosition[1] - 1, self.lightPosition[2], self.lightPosition[3])
            if key == 'j':
                self.lightPosition = (self.lightPosition[0], self.lightPosition[1] + 1, self.lightPosition[2], self.lightPosition[3])
            if key == 'n':
                self.lightPosition = (self.lightPosition[0], self.lightPosition[1], self.lightPosition[2] - 1, self.lightPosition[3])
            if key == 'm':
                self.lightPosition = (self.lightPosition[0], self.lightPosition[1], self.lightPosition[2] + 1, self.lightPosition[3])
        except:
            pass
        glutPostRedisplay()

    def getCanonicalForm(self,pointOne, pointTwo, pointThree):  # Просто считаю определитель для опеределения канонической формы плоскости
        x1 = pointOne[0]
        y1 = pointOne[1]
        z1 = pointOne[2]

        x2 = pointTwo[0]
        y2 = pointTwo[1]
        z2 = pointTwo[2]

        x3 = pointThree[0]
        y3 = pointThree[1]
        z3 = pointThree[2]

        result = [0, 0, 0, 0]  # ax+by+cz+d=0
        result[0] = (y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
        result[1] = -((x2-x1)*(z3-z1)-(z2-z1)*(x3-x1))
        result[2] = (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
        result[3] = -x1*result[0] - y1*result[1] - z1*result[2]

        return result

    def getPointInside(self):
        count = 0
        for face in self.faces:
            count += len(face)
            temp = list(zip(*face))
            for i in range(3):
                self.point[i] += sum(temp[i])
        self.point = [element/count for element in self.point]

    def getT(self,plane, pointOne, pointTwo):

        a = plane[0]
        b = plane[1]
        c = plane[2]
        d = plane[3]

        x1 = pointOne[0]
        y1 = pointOne[1]
        z1 = pointOne[2]

        x2 = pointTwo[0]
        y2 = pointTwo[1]
        z2 = pointTwo[2]

        t = (-d-a*x1-b*y1-c*z1)/(a*(x2-x1)+b*(y2-y1)+c*(z2-z1))

        return t

    def initFigure(self):
        glLineWidth(5)
        # z 
        glColor3f(0.0,0.0,1.0) # blue z
        glBegin(GL_LINES)
        glVertex3f(self.lightPosition[0], self.lightPosition[1] ,self.lightPosition[2])
        glVertex3f(self.lightPosition[0] + 0.1, self.lightPosition[1],self.lightPosition[2])

        glVertex3f(self.lightPosition[0], self.lightPosition[1] ,self.lightPosition[2])
        glVertex3f(self.lightPosition[0] - 0.1, self.lightPosition[1] + 0.1,self.lightPosition[2])

        glVertex3f(self.lightPosition[0], self.lightPosition[1] ,self.lightPosition[2])
        glVertex3f(self.lightPosition[0] - 0.1, self.lightPosition[1] - 0.1,self.lightPosition[2])
        glEnd()
        glFlush()
        for face in self.faces:
            cannonicalFrom = self.getCanonicalForm(face[0], face[1], face[2])
            t = self.getT(cannonicalFrom, self.point, self.eye)
            self.drawCoordinates()
            if 0 <= t <= 1:
                glBegin(GL_POLYGON)
                glColor3f(255, 215, 0)
                # glColor3f(0.5, 0.5, 0.5)
                glNormal3f(cannonicalFrom[0], cannonicalFrom[1], cannonicalFrom[2])  # Нормаль к плоскости, направлена наружу
                for vertex in face:
                    glVertex3dv(vertex)
                glEnd()
                glBegin(GL_LINE_LOOP)
                glColor3f(255, 215, 0)
                for vertex in face:
                    glVertex3dv(vertex)
                glEnd()
    
    def draw(self):
        self.getPointInside()
        self.initWindow()
        glutMainLoop()

    def initGL(self,Width, Height):
        glClearColor(0, 0, 0, 1.0)  # Цвет фона
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_CULL_FACE)  # Отрисовывается только видимая сторона плоскости
        glEnable(GL_LIGHTING)  # Включаем расчет освещения
        glEnable(GL_LIGHT0)  # Включаем источник
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)  # Разрешаем режим освещенности для двух сторон грани
        # glEnable(GL_COLOR_MATERIAL)  # Разрешаем цвет у материала
        glEnable(GL_NORMALIZE)  # Нормализуем нормали во избежание артефактов

    def draw3DScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient)  # Интенсивность освещения

        glLoadIdentity()

        gluLookAt(self.eye[0], self.eye[1], self.eye[2], 0, 0, 0, 0, 1, 0)

        # Настройка свойств источника света
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightPosition)  # Положение направленного источника света
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (0.0, 0.0, 1.0))  # Его направление
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))  # Интенсивность зеркального света
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.lightColor)  # Цвет света

        # Настройка свойств материала
        # Далее все идет только для внешней части (Front), т.к. только она и отрисовывается
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.lightColor)  # Отвечает за рассеивание материалом света с определенным цветом
        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.7, 0.7, 0.7, 1.0))  # Отвечает за затемнение цвета

        self.initFigure()

        glutSwapBuffers()

    def initWindow(self):
        global window

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(500, 100)

        window = glutCreateWindow(b"Task6")

        glutDisplayFunc(self.draw3DScene)
        # glutIdleFunc(draw3DScene)
        glutKeyboardFunc(self.keyPressed)
        self.initGL(800, 800)

    def get_XYZ(self,line1_entry,line2_entry,line3_entry):
        amount = int(line1_entry.get())
        self.eye[0] = amount
        amount1 = int(line2_entry.get())
        self.eye[1] = amount1
        amount2 = int(line3_entry.get())
        self.eye[2] = amount2
        
    def get_LP(self,line4_entry,line5_entry,line6_entry):
        amount = int(line4_entry.get())
        self.eye[0] = amount
        amount1 = int(line5_entry.get())
        self.eye[1] = amount1
        amount2 = int(line6_entry.get())
        self.eye[2] = amount2


    def choose_fig(self,figChoice):
        if figChoice.get() == 0:
            self.faces = (
         ((0, 0, 0), (0, 3, 0), (3, 3, 0), (3, 0, 0)),
         ((0, 0, 0), (0, 3, 0), (0, 3, 3), (0, 0, 3)),
         ((3, 0, 3), (3, 3, 3), (3, 3, 0), (3, 0, 0)),
         ((0, 3, 3), (0, 3, 0), (3, 3, 0), (3, 3, 3)),
         ((0, 0, 0), (3, 0, 0), (3, 0, 3), (0, 0, 3)),
         ((0, 0, 3), (3, 0, 3), (3, 3, 3), (0, 3, 3)))
            
        elif figChoice.get() == 1:
            self.faces = (
        ((0, 0, 0), (3, 0, 0), (3, 0, 3), (0, 0, 3)),
        ((0,0,0),(0,0,3),(1.5,3,1.5)),
        ((3,0,0),(0,0,0),(1.5,3,1.5)),
        ((3,0,3),(3,0,0),(1.5,3,1.5)),
        ((0,0,3),(3,0,3),(1.5,3,1.5)))
            
        elif figChoice.get() == 2:
            self.faces = (
        ((0,0,0),(3,0,1.5),(0,0,3)),
        ((0,0,0),(0,3,0),(3,3,1.5),(3,0,1.5)),
        ((3,3,1.5),(0,3,3),(0,0,3),(3,0,1.5)),
        ((0,3,3),(0,3,0),(0,0,0),(0,0,3)),
        ((0,3,0),(0,3,3),(3,3,1.5)))

        elif figChoice.get() == 3:
            self.faces = (
        ((0,0,3),(0,0,0),(1.5,-3,1.5)),
        ((0,0,0),(3,0,0),(1.5,-3,1.5)),
        ((3,0,0),(3,0,3),(1.5,-3,1.5)),
        ((3,0,3),(0,0,3),(1.5,-3,1.5)),
        ((0,0,0),(0,0,3),(1.5,3,1.5)),
        ((3,0,0),(0,0,0),(1.5,3,1.5)),
        ((3,0,3),(3,0,0),(1.5,3,1.5)),
        ((0,0,3),(3,0,3),(1.5,3,1.5)))

        elif figChoice.get() == 4:
            self.faces = (
         ((0, 0, 0), (0, 6, 0), (3, 6, 0), (3, 0, 0)),
         ((0, 0, 3),(0, 6, 3),(0, 6, 0),(0, 0, 0)),
         ((3, 0, 0),(3, 6, 0),(3, 6, 3),(3, 0, 3)),
         ((3, 6, 3),(3, 6, 0),(0, 6, 0),(0, 6, 3)),
         ((0, 0, 0), (3, 0, 0), (3, 0, 3), (0, 0, 3)),
         ((0, 0, 3), (3, 0, 3), (3, 6, 3), (0, 6, 3)))

    def drawCoordinates(self):
 
        glColor3f(1.0,0.0,0.0) # red x
        glBegin(GL_LINES)
        # x aix
    
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(10.0, 0.0, 0.0)

        # arrow
        glVertex3f(10.0, 0.0, 0.0)
        glVertex3f(9.0, 1.0, 0.0)
    
        glVertex3f(10.0, 0.0, 0.0)
        glVertex3f(9.0, -1.0, 0.0)
        glEnd()
        glFlush()
    
        glColor3f(1.0,0.0,0.0) # red x
        glBegin(GL_LINES)
        # x name
        glVertex3f(12.0, 0.0, 0.0)
        glVertex3f(11.0, 1.0, 0.0)

        glVertex3f(12.0, 0.0, 0.0)
        glVertex3f(11.0, -1.0, 0.0)

        glVertex3f(12.0, 0.0, 0.0)
        glVertex3f(13.0, 1.0, 0.0)

        glVertex3f(12.0, 0.0, 0.0)
        glVertex3f(13.0, -1.0, 0.0)
        glEnd()
        glFlush()
    
        # y 
        glColor3f(0.0,1.0,0.0) # green y
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 10.0, 0.0)
    
        # arrow
        glVertex3f(0.0, 10.0, 0.0)
        glVertex3f(1.0, 9.0, 0.0)
    
        glVertex3f(0.0, 10.0, 0.0)
        glVertex3f(-1.0, 9.0, 0.0)
        glEnd()
        glFlush()
    
        glColor3f(0.0,1.0,0.0) # red y
        glBegin(GL_LINES)
        # y name
        glVertex3f(0.0, 11.0, 0.0)
        glVertex3f(0.0, 12.0, 0.0)

        glVertex3f(0.0, 12.0, 0.0)
        glVertex3f(1.0, 13.0, 0.0)

        glVertex3f(0.0, 12.0, 0.0)
        glVertex3f(-1.0, 13.0, 0.0)

        glEnd()
        glFlush()


        # z 
        glColor3f(0.0,0.0,1.0) # blue z
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0 ,0.0 )
        glVertex3f(0.0, 0.0 ,10.0 )
    
        # arrow
        glVertex3f(0.0, 0.0 ,10.0 )
        glVertex3f(0.0, 1.0 ,9.0 )
    
        glVertex3f(0.0, 0.0 ,10.0 )
        glVertex3f(0.0, -1.0 ,9.0 )
        glEnd()
        glFlush()

        glColor3f(0.0,0.0,1.0) # blue z
        glBegin(GL_LINES)
        # z name
        glVertex3f(-1.0, 1.0, 11.0)
        glVertex3f(1.0, 1.0, 11.0)

        glVertex3f(-1.0, -1.0, 11.0)
        glVertex3f(1.0, -1.0, 11.0)

        glVertex3f(1.0, 1.0, 11.0)
        glVertex3f(-1.0, -1.0, 11.0)

        glEnd()
        glFlush()

def main():
    FG = Fong()
    #FG.getPointInside()
    #FG.initWindow()
    #glutMainLoop()

    global root
    # Cоздаём главное окно
    root = Tk()
    # Ширина экрана
    w = root.winfo_screenwidth() 
    # Высота экрана
    h = root.winfo_screenheight() 
    w = w//2 - 300
    h = h//2 - 200
    root.geometry('+{}+{}'.format(w, h))
    line123_infoLabel = Label(root, text="Введите координаты X,Y,Z точки взгляда: ",font=("Consolas", 10, "bold"))
    line1_entry = Entry(root,width=10)
    line2_entry = Entry(root,width=10)
    line3_entry = Entry(root,width=10)
    line3_but = Button(root,text="Ввести", command= lambda: FG.get_XYZ(line1_entry,line2_entry,line3_entry))
    line456_infoLabel = Label(root, text="Введите координаты X,Y,Z источника света: ",font=("Consolas", 10, "bold"))
    line4_entry = Entry(root,width=10)
    line5_entry = Entry(root,width=10)
    line6_entry = Entry(root,width=10)
    line6_but = Button(root,text="Ввести", command= lambda: FG.get_LP(line4_entry,line5_entry,line6_entry))
    
    # Создаём переменную-флаг принимающюю целый тип [0..4]
    choice = IntVar()
    choice.set(0)
    figChoice = IntVar()
    figChoice.set(0)
    cube_but = Radiobutton(root,text="Куб", variable=figChoice, value=0)
    pyram_but = Radiobutton(root,text="Пирамида", variable=figChoice, value=1)
    prism_but = Radiobutton(root,text="Призма", variable=figChoice, value=2)
    oct_but = Radiobutton(root,text="Октаэдр", variable=figChoice, value=3)
    pll_but = Radiobutton(root,text="Параллелепипед", variable=figChoice, value=4)
    fig_but = Button(root,text="Выбрать", command= lambda: FG.choose_fig(figChoice))
    draw1_but = Button(root,text="Отобразить", command= lambda: FG.draw())
    #restart_but = Button(root,text="Перезапустить приложение", command= lambda: refresh())

    line123_infoLabel.pack(side=tkinter.TOP)
    line1_entry.pack(side=tkinter.TOP)
    line2_entry.pack(side=tkinter.TOP)
    line3_entry.pack(side=tkinter.TOP)
    line3_but.pack(side=tkinter.TOP)
    line456_infoLabel.pack(side=tkinter.TOP)
    line4_entry.pack(side=tkinter.TOP)
    line5_entry.pack(side=tkinter.TOP)
    line6_entry.pack(side=tkinter.TOP)
    line6_but.pack(side=tkinter.TOP)

    cube_but.pack(side=tkinter.LEFT)
    pyram_but.pack(side=tkinter.LEFT)
    prism_but.pack(side=tkinter.LEFT)
    oct_but.pack(side=tkinter.LEFT)
    pll_but.pack(side=tkinter.LEFT)
    fig_but.pack(side=tkinter.LEFT)
    draw1_but.pack(side=tkinter.TOP)

    root.title("Выявление невидимых граней и рёбер")
    root.mainloop()


if __name__ == '__main__':
    #def refresh():
    #    root.destroy()
    #    main()

    main()