@download_page.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "POST":
        data = request.form
        requested_key = data.get("download_id")
        if requested_key != None:
            query = sa.select(File.filekey)
            valid_key_list = db.session.scalars(query).all()
            if requested_key in valid_key_list:
                upload_dir = current_app.config["UPLOAD_DIRECTORY"]
                query = sa.select(File).where(File.filekey == requested_key)
                file = db.session.scalar(query)
                if file is None:
                    flash("Incorrect Filekey")
                    return redirect(url_for('download.download'))
                return_file = f'{upload_dir}{file.filename}'
                return send_file(return_file, as_attachment=True)
            else:
                return abort(403)
        else:
            return abort(422)
    elif request.method == "GET":
        return render_template("download.html")