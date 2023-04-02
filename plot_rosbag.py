def plot_rosbag(full_path=None):
    """
    Plots graph from rosbag data
    Input:
        full_path (optional): path to the rosbag
    Output:
        None
        Displays graph 
    Written by Mukil Saravanan.
    """
    import rosbag
    import matplotlib.pyplot as plt
    
    if full_path is None:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        full_path = filedialog.askopenfilename(filetypes=[("ROS Bag Files", "*.bag")])
    
    bag = rosbag.Bag(full_path)
    topics = bag.get_type_and_topic_info()[1].keys()
    print("Available Topics:")
    for i, topic in enumerate(topics):
        print(f"{i}: {topic}")
    
    choice = int(input("Enter the topic number: "))
    topic = list(topics)[choice]
    
    topic_type = bag.get_type_and_topic_info()[1][topic].msg_type
    point_msg = roslib.message.get_message_class(topic_type)()
    print(point_msg)
    
    valid = False
    while not valid:
        param = input("Enter the parameter: ")
        try:
            ts = bag.read_messages(topics=topic, fields=[param])
            ts = [(t, msg.__getattribute__(param)) for t, _, msg in ts]
            ts = sorted(ts, key=lambda x: x[0])
            ts = [(t - ts[0][0]).to_sec(), v for t, v in ts]
            valid = True
        except:
            print(f"{param} is not valid")
    
    time = [t for t, _ in ts]
    data = [v for _, v in ts]
    
    full_topic = f"{topic}/{param.replace('.', '/')}"
    y_label_input = input("Enter the y label name,unit (Enclose within quotes): ")
    y_label_splitted = y_label_input.split(",")
    
    plt.plot(time, data)
    plt.title(full_topic)
    plt.xlabel("Time (in seconds)")
    plt.ylabel(f"{y_label_splitted[0]} (in {y_label_splitted[1]})")
    plt.xlim([0, max(time)])
    plt.legend([full_topic])
    plt.show()
