import pygame # needed because you need it

class mapping:

    camera = (0, 0) # virtual position of the camera
    original = (0, 0) # variable for the drag thing
    var = (0, 0) # while mouse pressed, show variation in the position of the mouse in each frame, when not pressed, shows camera's speed
    mouse_pressed = False # just to know if the user keeps pressing the mouse
    zoom = 1 # coeficient for the camera
    zoom_range = 0.2 # variation of the zoom per wheel move, recommended values: (0.1 - 0.9)
    dec = 0.01 # ratio of deceleration of the camera, it just reduces var values
    deceleration = 1 + dec # deceleration must be >1, or else it becames aceleration
    postzoom = 1 # virtual zoom value to make the smooth transition of the zoom
    zoomcoef = 0.05 # speed of the zoom animation
    xsize = 0 # size of the x-axis of the window of the dev
    ysize = 0 # size of the y-axis of the window of the dev
    resetable = True #enable/disable right click
    first = 1

    def map(alpha): # transforms virtual coordinates on real coordinates for the pygame.draw.something()
        x, y = alpha[0], alpha[1] # get's x and y values from the input
        new_x = (alpha[0] - mapping.camera[0]) / mapping.zoom + mapping.xsize/2 # finds real x
        new_y = (alpha[1] - mapping.camera[1]) / mapping.zoom + mapping.ysize/2 # finds real y
        # ^ the lines above: finds diference between virtual (x, y) and the position of the camera ...
        # ...in order to find the coordinates of the point according to the camera, ...
        # ...division between zoom for the zoom thing, ...
        # ...sums up xsize / 2 in order to center the camera in the window
        return (round(new_x), round(new_y)) # returns the values for the representation

    def esc(beta): # used for escalars, like radius
        beta = beta / mapping.zoom # no need to add something or to have somthing relative to somthing, just a coeficient
        return round(beta) # return the virtual value

    def unmap(alpha): # does all the stuff of map() but the other way around
        x, y = alpha[0], alpha[1]
        old_x = ((alpha[0] - mapping.xsize/2) * mapping.zoom) + mapping.camera[0]
        old_y = ((alpha[1] - mapping.ysize/2) * mapping.zoom) + mapping.camera[1]
        return (old_x, old_y)

    def size(x, y): # gets the dev window size
        mapping.xsize, mapping.ysize = x, y # gets the values

    def loop(): # mean loop, where all the controls and stuff is working
        for event in pygame.event.get(): # <- i guess you already know why this is here
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == mapping.first: # if the user presses right-click, then the program know the user pressed right-click
                    mapping.original = pygame.mouse.get_pos()
                    mapping.mouse_pressed = True # pygame only returns when the mouse is pressed, ...
                    # ...not while the mouse is pressed, so i need that

                if event.button == 3 and mapping.resetable: # resets camera's position and speed
                    mapping.camera = (0, 0)
                    mapping.var = (0, 0)

                if event.button == 5: # if wheel up, it increases postzoom value
                    mapping.postzoom = mapping.zoom + mapping.zoom*mapping.zoom_range*1
                    # ^ it increases the zoom value according to the last zoom value and the zoom range, ...
                    # ...and if the zoom is IN (1) or OUT(-1)
                if event.button == 4: # if wheel up, it decreases postzoom value
                    mapping.postzoom = mapping.zoom + mapping.zoom*mapping.zoom_range*-1

            if event.type == pygame.MOUSEBUTTONUP: # it resets the mouse_pressed thing
                if event.button == mapping.first:
                    mapping.mouse_pressed = False

        #the following 5 lines are for the zoom stuff, to make it work
        b = mapping.unmap(pygame.mouse.get_pos()) # i would explain this but it is a nightmare so i'm out
        mapping.zoom += (mapping.postzoom - mapping.zoom) * mapping.zoomcoef
        a = pygame.mouse.get_pos()
        mapping.camera = (mapping.camera[0] + b[0] - mapping.unmap(a)[0],
                          mapping.camera[1] + b[1] - mapping.unmap(a)[1])

        if mapping.mouse_pressed: # this is for the camera movement while the mouse is pressed
            mapping.var = (mapping.original[0] - a[0], mapping.original[1] - a[1]) # it gets the variation of the position
            mapping.camera = (mapping.camera[0] + mapping.var[0] * mapping.zoom,
                              mapping.camera[1] + mapping.var[1] * mapping.zoom) # modifies the camera position according to...
                              # ...the zoom so the background move in the same way than tha mouse
            mapping.original = a # resets the original value
        else: # this stuf is for the smooth-motion of the camera after a drag
            mapping.var = (mapping.var[0] / mapping.deceleration,
                           mapping.var[1] / mapping.deceleration)
            # ^ still uses the variation, in this case speed, but it decreases it slowly
            mapping.camera = (mapping.camera[0] + mapping.var[0] * mapping.zoom,
                              mapping.camera[1] + mapping.var[1] * mapping.zoom)
            # ^ it moves the camera according to the speed or, wich is the same, the var


    def help(): # ya know, nobody is born known
        print("Still working") # it says still working


# P.D i know i could use arrays from NumPy son i could do all the vectorial math
# without calling the lists, but i dont know very well how to work with them
# i'm learning, hope you're learning too

#now keep enjoying Python <3
