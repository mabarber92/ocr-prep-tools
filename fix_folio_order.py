from pdf_image_split_poppler import splitPdf
import os
import re
import shutil

def is_even(x):
    if x%2 == 0:
        return True
    else:
        return False

def reverse_image_list(image_path_dict, in_dir, out_dir, xml_list = None, first_folio=1):
    for idx, image_path in enumerate(reversed(sorted(list(image_path_dict.keys()))[first_folio-1:])):
        rename_and_copy(image_path_dict[image_path], in_dir, out_dir, idx)
        if xml_list is not None:
            if image_path_dict[image_path].split(".png") in xml_list:
                rename_and_copy(image_path_dict[image_path], in_dir, out_dir, idx, extension=".xml")


def rename_and_copy(image_file, old_dir, new_dir, new_number, extension=".png", page_splitter="_"):
    image_file = ".".join(image_file.split(".")[:-1]) + extension
    image_name = page_splitter.join(image_file.split(page_splitter)[:-1])
    new_image_name = image_name +  "{}{}{}".format(page_splitter, new_number, extension)
    existing_path = os.path.join(old_dir, image_file)
    new_path = os.path.join(new_dir, new_image_name)
    shutil.copyfile(existing_path, new_path)

def fix_folio_order(out_path, images=None, pdf=None, pattern="flip-bi-fold", first_folio=1, xml=False, bi_fold_start = 'even'):
    """Pattern can be 'flip-bi-fold' or 'reversed'
    flip-bi-fold assumes that the document is generally in the correct order but that the pages in each bi-fold have flipped: [2,1,4,3,6,5]
    reversed means the whole volume has been put together in the wrong order: [6,5,4,3,2,1]
    XML Functionality broken as we need to open and change the xml themselves to ensure matching of images to xmls
    """

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    if pdf is not None:
        images = os.path.join(out_path, "original-images/")
        if not os.path.exists(images):
            os.mkdir(images)
        out_path = os.path.join(out_path, "images_out")
        if not os.path.exists(out_path):            
            os.mkdir(out_path)
        splitPdf(pdf, images)
    elif images is None:
        print("No path to input file - try again")
        exit()

    path_list = os.listdir(images)

    # Create list that only contains image files
    image_path_dict = {}
    for path in path_list:
        if path.split(".")[-1] == "png":
            image_no = int(path.split(".")[1].split("_")[-1])
            image_path_dict[image_no] = path


    xml_list = []
    
    if xml:
        for name in path_list:
            print(name)
            if re.search(r"\.xml", name):
                xml_list.append(name.split(".xml")[0])
    else:
        xml_list = None

    if pattern == 'reversed':
        reverse_image_list(image_path_dict, images, out_path, xml_list)

    if pattern == 'flip-bi-fold':
        # Create bi-folds
        image_path_keys = sorted(list(image_path_dict.keys())[first_folio-1:])
        total_files = len(image_path_keys)
        bifold_list = []
        for idx, item in enumerate(image_path_keys):
            if idx == total_files-1:
                bifold = [image_path_dict[item]]
                bifold_list.append(bifold)
            elif bi_fold_start == 'even' and is_even(idx):
                bifold = [image_path_dict[item], image_path_dict[item+1]]                
                bifold_list.append(bifold)
            elif bi_fold_start == 'odd':
                if not is_even(idx):
                    bifold = [image_path_dict[item], image_path_dict[item+1]]                
                    bifold_list.append(bifold)
                if idx == 0:
                    bifold = [image_path_dict[item]]
                    bifold_list.append(bifold)
        
        print(bifold_list)
        page_counter = 0
        for idx, bifold in enumerate(bifold_list):
            if len(bifold) > 1:
                rename_and_copy(bifold[1], images, out_path, page_counter)
                if xml_list is not None:                    
                    if bifold[0].split(".png")[0] in xml_list:
                        rename_and_copy(bifold[1], images, out_path, page_counter, extension='.xml')
                page_counter += 1
            rename_and_copy(bifold[0], images, out_path, page_counter)
            if xml_list is not None:
                if bifold[0].split(".png")[0] in xml_list:
                    rename_and_copy(bifold[0], images, out_path, page_counter, extension='.xml')
            page_counter += 1



if __name__ == "__main__":
    images = "./maqrizi_notebook/export_doc238_maqrizi_notebook_alto_202411211757/"
    out_folder = "./maqrizi_notebook/images_out/"
    fix_folio_order(out_folder, images=images, bi_fold_start='odd')
