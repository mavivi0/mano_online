# frozen_string_literal: true

# Makes content/ the single source of truth for the site. Nothing in content/ is
# published as-is; this plugin hands each file to the part of al-folio that uses it:
#
#   profile.yml -> site name and description, homepage subtitle and contact icons
#                  (bin/build-cv also reads it for the PDF header)
#   bio.md      -> homepage text (rendered by _pages/about.md)
#   cv.yml      -> web CV (_pages/cv.md) and PDF CV
#   papers.bib  -> publications page, homepage selection, CV publications
#                  (read directly by jekyll-scholar, see `scholar.source` in _config.yml)
#   photo.jpg   -> profile photo (assets/img/prof_pic.jpg is a symlink to it)
#
# It also builds the CV PDF with bin/build-cv whenever content/ changes and
# publishes it at /assets/pdf/cv.pdf.

require "digest"
require "open3"

module ContentFolder
  DIR = "content"
  PDF_URL = "/assets/pdf/cv.pdf"

  # The PDF is built into Jekyll's cache, so it is copied into _site like any other file.
  class PdfFile < Jekyll::StaticFile
    def initialize(site, path)
      super(site, File.dirname(path), "", File.basename(path))
    end

    def destination(dest) = File.join(dest, PDF_URL)
    def url = PDF_URL
  end

  module_function

  def read(site, name) = File.read(site.in_source_dir(DIR, name))
  def load_yaml(site, name) = SafeYAML.load(read(site, name))

  def apply(site)
    profile = load_yaml(site, "profile.yml")
    cv = load_yaml(site, "cv.yml")

    site.config["first_name"] = profile["first_name"]
    site.config["last_name"] = profile["last_name"]
    site.config["description"] = profile["description"] if profile["description"]
    site.config["scholar"]["first_name"] = [profile["first_name"]]
    site.config["scholar"]["last_name"] = [profile["last_name"]]

    links = { "email" => profile["email"] }.merge(profile["links"] || {}).merge("cv_pdf" => PDF_URL)
    site.data["socials"] = links.reject { |_, value| value.to_s.strip.empty? }
    site.data["profile"] = profile.merge("bio" => read(site, "bio.md"))
    # Only the sections: the homepage already shows the contact details, and with them
    # al-folio would add a "Contact Information" card to the top of the web CV.
    site.data["cv"] = { "cv" => { "sections" => cv["sections"] } }

    site.pages.each do |page|
      next unless page.data["layout"] == "about"

      page.data["subtitle"] = profile["headline"]
      page.data["profile"]["more_info"] = "<p>#{profile["location"]}</p>" if page.data["profile"]
    end

    # content/ is input only: don't copy it into the site.
    site.static_files.reject! { |file| file.relative_path.start_with?("/#{DIR}/") }
    site.pages.reject! { |page| page.relative_path.start_with?("#{DIR}/") }
  end

  def build_pdf(site)
    inputs = Dir[site.in_source_dir(DIR, "*"), site.in_source_dir("_rendercv", "*"), site.in_source_dir("bin", "build-cv")]
    digest = Digest::SHA256.hexdigest(inputs.sort.map { |path| path + File.binread(path) }.join)
    cache = site.in_source_dir(".jekyll-cache", "cv-pdf")
    pdf = File.join(cache, "#{digest}.pdf")

    unless File.exist?(pdf)
      FileUtils.rm_rf(cache)
      Jekyll.logger.info "CV PDF:", "building with bin/build-cv"
      begin
        output, status = Open3.capture2e(ENV.fetch("PYTHON", "python3"), site.in_source_dir("bin", "build-cv"), "--out", pdf)
      rescue SystemCallError => e
        output, status = e.message, nil
      end
      unless status&.success?
        message = "could not build the CV PDF (python3 -m pip install -r requirements.txt?):\n#{output}"
        raise message if ENV["CV_PDF_REQUIRED"]

        Jekyll.logger.warn "CV PDF:", message
        return
      end
    end
    site.static_files << PdfFile.new(site, pdf)
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  ContentFolder.apply(site)
  ContentFolder.build_pdf(site)
end
